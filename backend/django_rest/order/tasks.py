"""Create your api tasks"""

from celery import shared_task
# from django.core.exceptions import ObjectDoesNotExist
from djmoney.money import Money

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from core.models import (PurchaseOrder, Promotion, POShipping, ShippingMethod,
                         POPayment, PaymentMethod, Address, Tax, Country,
                         ProductItem, POItem, POProfile)

from order.serializers import PurchaseOrderDetailsSerializer

import logging
# import requests

# Note: send_mail() method has the following parameters:
#
#       The 'subject', 'message', 'from_email' and 'recipient_list' parameters
#       are required.
#
#       1- subject: A string.
#       2- message: A string.
#       3- from_email: A string. If None, Django will use the value of the
#                      'DEFAULT_FROM_EMAIL' setting.
#                      You can modify the sender name if you want a pretty
#                      email name. Add a desired name in the beginning in
#                      double quotes and an email address the email will be
#                      (sent from) in the end in <> like this:
#                      ”Desired name” <email@example.com>.
#       4- recipient_list: A list of strings, each an email address. Each
#                          member of recipient_list will see the other
#                          recipients in the “To:” field of the email message.
#       5- fail_silently: A boolean. When it’s False, send_mail() will raise
#                         the smtplib.SMTPException if an error occurs.
#       6- auth_user: The optional username to use to authenticate to the SMTP
#                     server. If this isn’t provided, Django will use the value
#                     of the EMAIL_HOST_USER setting.
#       7- auth_password: The optional password to use to authenticate to the
#                         SMTP server. If this isn’t provided, Django will use
#                         the value of the EMAIL_HOST_PASSWORD setting.
#       8- connection: The optional email backend to use to send the mail. If
#                      unspecified, an instance of the default backend will be
#                      used.
#       9- html_message: If html_message is provided, the resulting email will
#                        be a multipart/alternative email with message as the
#                        text/plain content type and html_message as the
#                        text/html content type.
#
#      * The return value of the method will be the number of successfully
#        delivered messages (which can be 0 or 1 since it can only send one
#        message).
#
#      * It’s good practice to send equivalent content in your plain-text body
#        and the html version, so, the classic example is to send both text and
#        HTML versions of a message. With Django’s email library, you can do
#        this using the 'EmailMultiAlternatives' class. This subclass of
#        'EmailMessage' has an attach_alternative() method for including extra
#        versions of the message body in the email.

# Note: get_template() or any other method of 'loader' module will depend on
#       'DIRS' parameter of 'TEMPLATES' list variable in 'settings.py' file for
#       looking for the given template name.


@shared_task
def set_purchase_order_details(po_code, **extra_fields):
    """Set order fields value"""

    # Important: This celery job method depend on the check process and
    #            configuring correct values for its parameters.

    # Note: by default 'po_profile' instance is already created in purchase
    #       order create APIView, So we need to set following details to
    #       purchase order:
    #
    #       1- promotion instance as foreign key if provided.
    #       2- po_shipping instance as foreign key.
    #       3- po_payment instance as foreign key.
    #       4- tax instance as foreign key if exists.
    #

    # extra_fields as kwargs could contain:
    #
    # 1- promotion_title=<string_value>
    # 2- tax_title=<string_value>
    # 3- payment_details as dictionary:
    #    {
    #      "method": <value>, # the only thing required if payment
    #                         # method is not card.
    #      "card_details": {
    #                  "cardholder_name": <value>,
    #                  "card_number": <value>,
    #                  "card_expiry": <value>, # e.g, 12/24
    #                  "card_ccv": <value> # should be either 3 or 4 digits
    #      },
    #      "use_shipping_address": <value> # boolean, don't use quotes
    #      "billing": { # not required if 'use_shipping_address': true
    #            "personal_info": {
    #                          "first_name": <value>,
    #                          "last_name": <value>,
    #                          "email": <value>, # not required
    #                          "phone_number": <value>
    #             },
    #             "country": { # possible, one of them
    #                     "iso_code": <value>,
    #                     "title": <value>
    #             },
    #             "address_details": {
    #                           "address1": <value>,
    #                           "address2": <value>,
    #                           "region": <value>,
    #                           "city": <value>,
    #                           "postal_code": <value>
    #             }
    #      }
    #    }
    # 4- shipping_details as dictionary:
    #    {
    #      'method': <value>, # method title
    #      'cost': <value>,
    #      'cost_currency': <value>,
    #      'country_iso_code': <value>,
    #      'address1': <value>,
    #      'address2': <value>,
    #      'city': <value>,
    #      'region': <value>,
    #      'postal_code': <value>
    #    }
    # 5- po_items as list of items as dictionary:
    #    [
    #      {
    #        "sku": <value>,
    #        "quantity": <value>
    #      }
    #    ]

    # Initialize global variable for purchase order
    purchase_order = None

    try:

        def set_address(iso_code, address1, address2, city, region,
                        postal_code):
            """Return and Search for address instance and create it if it's not
             exists"""

            # Get the country instance
            country = Country.objects.get(iso_code=iso_code)

            # Get or create address instance
            # Note: here we can't use get_or_create() because Address model
            #       doesn't use unique constraint, so it's possible to retrieve
            #       multiple records from database.
            address_instance = Address.objects.filter(
                country=country,
                address1__iexact=address1,
                address2__iexact=address2,
                city__iexact=city,
                region__iexact=region,
                postal_code__iexact=postal_code
            ).distinct().first()

            if not address_instance:
                # In case no address instance has retrieved, create new one.
                address_instance = Address.objects.create(
                    country=country,
                    address1=address1,
                    address2=address2,
                    city=city,
                    region=region,
                    postal_code=postal_code
                )

            # Return address instance.
            return address_instance

        ###################################################################
        # Get purchase order instance.
        # Note: we use QuerySet filter() method not Model get(), because the
        #       update() method which can't be use with model instance due it's
        #       a QuerySet method not Model manager method.
        #       also note that first() method return a Model instance.
        purchase_order = PurchaseOrder.objects.get(po_code=po_code)

        ###################################################################
        # Set po_shipping instance:

        # Get shipping details from extra fields
        shipping_details = extra_fields['shipping_details']

        # 1- Get shipping method instance.
        shipping_method = ShippingMethod.objects.get(
            title=shipping_details['method']
        )

        # 2- Set shipping cost value with its currency as Money.
        cost = Money(
            shipping_details['cost'],
            shipping_details['cost_currency']
        )

        # 3- Set or create shipping address.

        # Get required values from extra fields shipping details
        sh_country_iso_code = shipping_details['country_iso_code']
        sh_address1 = shipping_details['address1']
        sh_address2 = shipping_details.get('address2', '')
        sh_city = shipping_details['city']
        sh_region = shipping_details['region']
        sh_postal_code = shipping_details.get('postal_code', '')

        # Call set_address() method.
        shipping_address = set_address(
            iso_code=sh_country_iso_code,
            address1=sh_address1,
            address2=sh_address2,
            city=sh_city,
            region=sh_region,
            postal_code=sh_postal_code
        )

        # 4- Create 'POShipping' instance.
        # Info: in create process of instance you should pass foreign key value
        #       as instance and never use look_up keys.
        po_shipping = POShipping.objects.create(
            shipping_method=shipping_method,
            address=shipping_address,
            cost=cost
        )

        # Set po_shipping instance to 'po_shipping' field of purchase order.
        purchase_order.po_shipping = po_shipping

        ###################################################################
        # Set POPayment instance:

        # Get payment details from extra fields
        payment_details = extra_fields['payment_details']

        # 1- Get payment method instance.
        payment_method = PaymentMethod.objects.get(
            title=payment_details['method']
        )

        # 2- In case the payment method is card.

        # Initialize variable to hold scripted card number.
        scripted_card_num = ''
        use_shipping_address = True
        po_profile = None
        billing_address = None

        if payment_method.is_card:

            # If you choose to make the transaction process with related
            # payment card api inside task job NOT in the view, then you need
            # to pass all the required details for this task to execute
            # transaction process. While for not card payment, you should do
            # the transaction on frontend like Amazon Pay.

            # Get card details from payment details.
            card_details = payment_details['card_details']

            # Then create a string of scripted card number from the passed
            # payment details.

            # Get the card number
            card_number = card_details.get('card_number', "")

            # Get length
            len_card_num = len(card_number)

            if len_card_num > 4:
                # Create from card number a string looks like: *****6789
                scripted_card_num = (len_card_num - 4) * '*' + card_number[-4:]

            # Get value of use shipping address or True as default.
            use_shipping_address = payment_details.get(
                'use_shipping_address',
                True
            )

            # Check whether 'use_shipping_address' is true or not.
            if not use_shipping_address:
                # In case not, then we need to get or create address that
                # represent billing address
                pa_country = payment_details['billing']['country']
                pa_addr_details = payment_details['billing']['address_details']

                # Call set_address() method.
                billing_address = set_address(
                    iso_code=pa_country['iso_code'],
                    address1=pa_addr_details['address1'],
                    address2=pa_addr_details.get('address2', ''),
                    city=pa_addr_details['city'],
                    region=pa_addr_details['region'],
                    postal_code=pa_addr_details.get('postal_code', '')
                )
            else:
                # in case use sipping address is True.
                billing_address = shipping_address

            # Create billing address profile if not exists.

            # Check if personal info details is not provided in billing
            # address, then use purchase order related po_profile details.
            pa_personal_info = payment_details['billing']['personal_info']

            b_addr_first_name = pa_personal_info.get(
                'first_name',
                purchase_order.po_profile.first_name
            )
            b_addr_last_name = pa_personal_info.get(
                'last_name',
                purchase_order.po_profile.last_name
            )
            b_addr_email = pa_personal_info.get(
                'email',
                purchase_order.po_profile.email
            )
            b_addr_phone_num = pa_personal_info.get(
                'phone_number',
                purchase_order.po_profile.phone_number
            )

            # Note: get_or_create() method return tuple where:
            #       1- first object is the instance that found or created.
            #       2- second object is Boolean value if instance has created.
            #
            #       By default, this is a case-sensitive method (exact) (as it
            #       should be, for the general case). To make the lookup
            #       (iexact) case-insensitive, you use <field_name>__iexact
            #       instead of <field_name>.
            #       You also need to give the get_or_create() method
            #       a 'defaults' parameter to use when creating the instance,
            #       that will be used in a get() call before create() where all
            #       lookups containing the lookup separator __ are stripped
            #       from the parameters passed to create().
            #
            # Info: also there is method update_or_create()
            po_profile = POProfile.objects.get_or_create(
                defaults={
                    'first_name': b_addr_first_name,
                    'last_name': b_addr_last_name,
                    'email': b_addr_email
                },
                first_name__iexact=b_addr_first_name,
                last_name__iexact=b_addr_last_name,
                email__iexact=b_addr_email,
                phone_number=b_addr_phone_num,
            )[0]

        # 3- Create POPayment instance.
        po_payment = POPayment.objects.create(
            use_shipping_address=use_shipping_address,
            card_number=scripted_card_num,
            payment_method=payment_method,
            po_profile=po_profile,
            address=billing_address
        )

        # Set po_payment instance to 'po_payment' field of purchase order.
        purchase_order.po_payment = po_payment

        ###################################################################
        # Set tax instance if provided.
        if extra_fields['tax_title']:
            # Get tax instance.
            tax = Tax.objets.get(title=extra_fields['tax_title'])

            # Set tax instance to 'tax' field of purchase order.
            purchase_order.tax = tax

        ###################################################################
        # Set promotion instance if provided.
        if extra_fields['promotion_title']:
            # Get promotion instance.
            promotion = Promotion.objects.get(
                title=extra_fields['promotion_title']
            )

            # Set promotion instance to 'promotion' field of purchase order.
            purchase_order.promotion = promotion

        ###################################################################
        # Create POItem instances that related to current purchase order.

        # initialize bulk list.
        po_item_bulk = []

        # Loop over the extra_fields 'po_items' list.
        for item in extra_fields['po_items']:

            # Get the product item instance using current item 'sku' value.
            product_item = ProductItem.objects.get(sku=item['sku'])

            # Note: because we are using bulk_create() to create POItem
            #       instances, we have to set 'price_per_unit' even it's set
            #       automatically in 'signals.py' file that due the fact of
            #       bulk_create() method which doesn't trigger any signal.

            # Set Money of either deal_price or list_price to 'price_per_unit'
            price_per_unit = product_item.deal_price or product_item.list_price

            # Append to bulk list a POItem variable.
            po_item_bulk.append(
                POItem(
                    purchase_order=purchase_order,
                    product_item=product_item,
                    quantity=item['quantity'],
                    price_per_unit=price_per_unit
                )
            )

        # Trigger bulk_create() method for the bulk list.
        # Note: we don't need to catch the new created records of POItem
        #       instance.
        POItem.objects.bulk_create(po_item_bulk)

        ##################################################################
        # Trigger save() method to purchase order instance with added values.
        purchase_order.save()

        ##################################################################
        # Receiver details
        to_email = purchase_order.po_profile.email
        first_name = purchase_order.po_profile.first_name
        last_name = purchase_order.po_profile.last_name
        from_email = '"Jamie & Cassie, Order Confirmation"' \
                     ' <noreply@jamieandcassie.store>'

        # Set context variables to pass to text template on render stage of
        # the file.
        text_context = {
            "first_name": str(first_name).capitalize(),
            "last_name": str(last_name).capitalize(),
            "po_code": po_code,
            "order_details_url": extra_fields['order_details_url']
        }

        # Render the text version for email body.
        text_content = render_to_string(
            template_name='order/text/order-confirm.txt',
            context=text_context
        )

        # Set context variables to pass to html template on render stage of
        # the file.
        # Note: here we don't pass context directly to the html file, we
        #       process the template through serializer in APIView class.
        # html_context = {
        #     "first_name": first_name,
        #     "last_name": last_name,
        #     "po_code": po_code
        # }

        # Serialize the purchase order instance.
        serializer_obj = PurchaseOrderDetailsSerializer(purchase_order)

        # Update the serialized object with extra key:value
        # Info: here we don't need such value, because serializer already
        #       has.
        # serializer_obj.update(
        #     {
        #         "order_details_url": extra_fields['order_details_url']
        #     }
        # )

        # Render the html version for email body.
        html_content = render_to_string(
            template_name='order/html/order-confirm.html',
            context=serializer_obj.data
        )

        # Initialize instance of EmailMultiAlternatives with text content
        # for email body.
        msg = EmailMultiAlternatives(
            subject=f'Order {po_code}',
            from_email=from_email,
            to=[to_email],
            body=text_content
        )

        # Attach an alternative content representation for email body.
        msg.attach_alternative(content=html_content, mimetype="text/html")

    except Exception as e:

        # Set purchase order status to be 'Error'.
        purchase_order.status = 'Error'

        # Trigger save() method to purchase order instance with added values.
        purchase_order.save()

        logging.exception(e)

    else:
        ###################################################################
        # If no exception is raised, send email of order confirm to the one who
        # made the purchase.

        # Send message with Anymail.
        try:
            msg.send(fail_silently=False)

        except Exception as e:
            # Here in case Anymail raise an exception while trying to send
            # the email, so you can define a way to deal with such
            # exception like sending an email to website support team.

            # Set purchase order status to be 'Error'.
            purchase_order.status = 'Error'

            # Trigger save() method to purchase order instance with added
            # values.
            purchase_order.save()

            logging.exception(e)
