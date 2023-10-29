"""Create your api Views"""

from rest_framework import views, status, generics
from rest_framework.response import Response
# from rest_framework.decorators import api_view, parser_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
# from rest_framework.generics import get_object_or_404

from cart.views import CartCheckApiView
from shipping.views import ShippingCheckAPIView
from payment.views import PaymentCheckApiView
from core.models import round_money, PurchaseOrder, POProfile
from order.tasks import set_purchase_order_details
from order import serializers, throttles

from django.urls import reverse
from decimal import Decimal
from django.conf import settings
# from rest_framework.settings import api_settings
# from rest_framework.exceptions import ParseError
# from rest_framework import renderers
# from rest_framework.parsers import BaseParser
# from rest_framework.utils import json
# import codecs

import logging
# import requests


# Important: you should know that 'HttpRequest' AKA 'request._request' can't be
#            used multiple times after it has been read by Django Rest
#            Framework 'View' parser class that will lead to call 'read()'
#            method which will change the '_request' object's property
#            '_read_started' to be 'True', and after that if you tried to use
#            'request.data' or 'request._request' will raise the exception:
#
#            RawPostDataException: You cannot access body after reading from
#                                  request's data stream
#
#            Because the 'request.body' is not accessible anymore due it counts
#            on the value of '_read_started' property, also not to mention that
#            the value of 'HttpRequest' has already been converted into
#            'stream' object and stored in the memory, so if you are going to
#            use the below code to call another 'APIView' from another
#            'APIView' will lead to such case:
#
#            from rest_framework import views
#            from rest_framework.response import Response
#
#            from A.views import A
#
#            class B(views.APIView):
#
#                def post(self, request, *args, **kwargs):
#
#                     # Note: as_view() method can automatically specify the
#                     #       HTTP method to use for calling view class as same
#                     #       current request method.
#                     http_response = A.as_view()(request._request)
#
#                     # So far so good, but if I want to access request.data
#                     # after calling A.as_view() will raise the exception.
#
#                     return Response(http_response.data)
#
#
#            There are multiple suggestions I found:
#            1- use Middleware to store the request.body to use it later in
#               case of need.
#            2- use a custom parser class that store raw data as property in
#               request object before converting it into stream object.
#
#            Both of them I found is a little bit complicated, so I changed the
#            way of calling another 'APIView' from certain DRF 'View', as
#            shown:
#
#            # Initialize a new instance of class view 'A'
#            a_view = A()
#
#            # Calling HTTP 'POST' method with DRF request object.
#            a_http_response = a_view.post(request)


# class BodySavingJSONParser(BaseParser):
#     """
#     Custom parser of JSON-serialized data.
#     """
#
#     # Info: parser is the one who convert raw HTTP request passed data into
#     #       accessible data while render is responsible for converting
#     #       serialized data to raw data that transfer back to as response.
#
#     # Note: you can't get value of added 'raw_value' property unless the
#     #       parser is called, and usually it's called when trying to get
#     #       value of 'request.data'.
#
#     media_type = 'application/json'
#     renderer_class = renderers.JSONRenderer
#     strict = api_settings.STRICT_JSON
#
#     def parse(self, stream, media_type=None, parser_context=None):
#         """
#         Parses the incoming bytestream as JSON and returns the resulting data
#         """
#         parser_context = parser_context or {}
#         encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)
#         request = parser_context.get('request')
#
#         try:
#             decoded_stream = codecs.getreader(encoding)(stream)
#             decoded_content = decoded_stream.read()
#             # Saving decoded request original body to raw_body
#             setattr(request, 'raw_body', decoded_content)
#             parse_constant = json.strict_constant if self.strict else None
#             return json.loads(decoded_content, parse_constant=parse_constant)
#         except ValueError as exc:
#             raise ParseError('JSON parse error - %s' % str(exc))


class PurchaseOrderCheckAPIView(views.APIView):
    """APIView for order"""

    # Specify the parser to be use in your view. DRF view default parsers are:
    # 1- JSONParser()
    # 2- FormParser()
    # 3- MultiPartParser()

    # parser_classes = [BodySavingJSONParser]

    # Get the default value for money decimal digits from 'api' settings.
    money_decimal_digits = settings.MONEY_DECIMAL_PLACES

    def post(self, request):
        """HTTP POST method"""

        # Data attribute value for this view POST method should be:
        # {
        #   "cart": {
        #        "items": [
        #              {
        #                "sku": <value>,
        #                "quantity": <value>
        #              } ...
        #         ]
        #   },
        #   "shipping": {
        #           "method": <value>,
        #           "personal_info": {
        #                        "first_name": <value>,
        #                        "last_name": <value>,
        #                        "email": <value>,
        #                        "phone_number": <value>
        #             },
        #            "country": { # possible, one of them
        #                   "iso_code": <value>,
        #                   "title": <value>
        #             },
        #            "address_details": {
        #                           "address1": <value>,
        #                           "address2": <value>,
        #                           "region": <value>,
        #                           "city": <value>,
        #                           "postal_code": <value>
        #             }
        #   },
        #   "payment": {
        #          "method": <value>, # the only thing required if payment
        #                             # method is not card.
        #          "card_details": {
        #              "cardholder_name": <value>,
        #              "card_number": <value>,
        #              "card_expiry": <value>, # e.g, 12/24
        #              "card_ccv": <value> # should be either 3 or 4 digits
        #
        #           },
        #          "use_shipping_address": <value> # boolean, don't use quotes
        #          "billing": { # not required if 'use_shipping_address': true
        #                 "personal_info": {
        #                              "first_name": <value>,
        #                              "last_name": <value>,
        #                              "phone_number": <value>
        #                   },
        #                  "country": { # possible, one of them
        #                        "iso_code": <value>,
        #                        "title": <value>
        #                   },
        #                  "address_details": {
        #                                 "address1": <value>,
        #                                 "address2": <value>,
        #                                 "region": <value>,
        #                                 "city": <value>,
        #                                 "postal_code": <value>
        #                   }
        #           }
        #   },
        #   "coupon": <value>, # not required
        #   "grand_total": <value>, # not required
        #   "price_currency": <value> # not required
        # }

        try:

            # First step, check cart items by calling /cart/check/ with HTTP
            # post request.

            cart_check_res = CartCheckApiView().post(request)

            if cart_check_res.status_code != status.HTTP_200_OK:
                # We need additional info about which api is causing the error.
                cart_check_res.data.update({
                    "api": "cart"
                })

                return Response(
                    cart_check_res.data,
                    status=cart_check_res.status_code
                )
            elif not cart_check_res.data.get('items', None):
                # In case cart was empty
                cart_check_res.data.update({
                    "message": "You can't create purchase order with empty "
                               "cart",
                    "api": "order"
                })
                return Response(
                    cart_check_res.data,
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get the info we need from cart api response if check went ok.
            subtotal_currency = cart_check_res.data['price_currency']
            subtotal_price_amount = cart_check_res.data['total_price_amount']

            # Second step:
            # 1- check shipping cost and
            # 2- check the requested shipping method and
            # 3- validate the shipping address by calling shipping cost view
            # 4- Get the shipping cost.

            shipping = request.data.get("shipping", None)
            shipping_check_res = ShippingCheckAPIView().post(
                request=request,
                data=shipping
            )

            if shipping_check_res.status_code != status.HTTP_200_OK:
                shipping_check_res.data.update({
                    "api": "shipping"
                })

                return Response(
                    shipping_check_res.data,
                    status=shipping_check_res.status_code
                )

            # Get the info we need from shipping api if check went ok.
            shipping_price_currency = shipping_check_res.data['price_currency']
            shipping_cost_amount = \
                shipping_check_res.data['shipping_cost_amount']

            ################################################################
            # Note: so far we don't have tax system, so we will ignore
            #       it's cost
            ################################################################

            if subtotal_currency != shipping_price_currency:
                return Response(
                    {
                        "message": "Error is occurred while trying to"
                                   " create the order where shipping"
                                   " cost currency is different from"
                                   " subtotal currency",
                        "shipping_cost_currency": shipping_price_currency,
                        "cart_subtotal_currency": subtotal_currency
                    },
                    status=status.HTTP_409_CONFLICT
                )

            # Third step, calculate the grand total.

            # Get Decimal value of shipping cost amount
            cost_a = Decimal(shipping_cost_amount)

            # Get Decimal value of subtotal amount
            subtotal_a = Decimal(subtotal_price_amount)

            # Find total price amount for (cart cost + shipping cost)
            total_amount = cost_a + subtotal_a

            # Set grand total price as money variable.
            grand_total = round_money(amount=total_amount)

            # Check that the grand total that calculated on server side is
            # equal to the 'grand_total' argument of request POST data if
            # exists while have same currency symbol, otherwise return error
            # if they are not equals.

            fr_grand_total = request.data.get("grand_total", None)
            fr_price_currency = request.data.get("price_currency", None)

            if fr_grand_total and fr_price_currency:

                if fr_grand_total != grand_total or \
                        fr_price_currency != grand_total.currency.code:

                    return Response(
                        {
                            "message": "The sent frontend grand total is not "
                                       "equal to value that calculated by "
                                       "the server",
                            "sent_price_currency": fr_price_currency,
                            "sent_grand_total_amount": fr_grand_total,
                            "price_currency": grand_total.currency.code,
                            "price_currency_symbol": settings.CURRENCY_SYMBOLS[
                                grand_total.currency.code
                            ],
                            "grand_total_amount": "{:.2f}".format(
                                round(
                                    grand_total.amount,
                                    self.money_decimal_digits
                                )
                            ),
                        },
                        status=status.HTTP_409_CONFLICT
                    )

            # Fourth step, payment process.

            # Get payment details from request POST data.
            payment = request.data.get("payment", None)
            payment_check_res = PaymentCheckApiView().post(
                request=request,
                data=payment
            )

            if payment_check_res.status_code != status.HTTP_200_OK:
                payment_check_res.data.update({
                    "api": "payment"
                })

                return Response(
                    payment_check_res.data,
                    status=payment_check_res.status_code
                )

            # In case everything went ok.
            return Response(
                {
                    'price_currency': grand_total.currency.code,
                    'price_currency_symbol': settings.CURRENCY_SYMBOLS[
                        grand_total.currency.code
                    ],
                    'grand_total_amount': "{:.2f}".format(
                        round(
                            grand_total.amount,
                            self.money_decimal_digits
                        )
                    ),
                    'cart_details': cart_check_res.data,
                    'shipping_details': shipping_check_res.data,
                    'payment_details': payment_check_res.data,
                    'api': 'order'
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logging.exception(e)

            return Response(
                {
                    "message": "Error is occurred while trying to create the "
                               "order"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PurchaseOrderCreateAPIView(generics.CreateAPIView):
    """APIView for create order"""

    # Note: I prefer to make payment transaction within the celery job.

    serializer_class = serializers.PurchaseOrderSerializer
    # Info: so far the order process work with no authentication, so the
    #       choosing throttle class will be related to anonymous user.
    throttle_classes = [throttles.AnonMinThrottle, throttles.UserMinThrottle]
    queryset = PurchaseOrder.objects.all()
    purchase_order_check_res = None

    def post(self, request, *args, **kwargs):
        """Override the supper class HTTP post method"""

        # Note: This method related to 'CreateAPIView' of 'generics' view that
        #       is the first method to trigger when HTTP POST request caught.
        self.purchase_order_check_res = PurchaseOrderCheckAPIView().post(
            request
        )

        if self.purchase_order_check_res.status_code != status.HTTP_200_OK:
            return Response(
                self.purchase_order_check_res.data,
                status=self.purchase_order_check_res.status_code
            )
        else:
            return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Check that purchase order profile is not exist to create new one
        otherwise use the existing POProfile model instance"""

        # Info: perform_create() method of 'CreateModelMixin' that implement
        #       by 'generics.CreateAPIView' does the actual work of saving
        #       an instance - literally, all it does is call serializer.save()
        #       by default.
        #       While create() method for same class does more work, by
        #       instantiating and validating the serializer and setting up the
        #       response.
        #       So, perform_create() is called by create() method that return
        #       HTTP response with '201_CREATED' of status code.

        # Note: 'po_profile' foreign key field of 'PurchaseOrder' instance
        #       should not be null when create new instance that because we
        #       count on its value in signals.py file to generate new 'po_code'

        # Get check response data value
        check_res_data = self.purchase_order_check_res.data

        # Get shipping personal info.
        profile_info = check_res_data['shipping_details']['personal_info']

        # Note: get_or_create() method return tuple where:
        #       1- first object is the instance that found or created.
        #       2- second object is Boolean value if instance has created.
        #
        #       By default, this is a case-sensitive method (exact) (as it
        #       should be, for the general case). To make the lookup (iexact)
        #       case-insensitive, you use <field_name>__iexact instead of
        #       <field_name>.
        #       You also need to give the get_or_create() method a 'defaults'
        #       parameter to use when creating the instance, that will be used
        #       in a get() call before create() where all lookups containing
        #       the lookup separator __ are stripped from the parameters passed
        #       to create().
        #
        # Info: also there is method update_or_create()
        po_profile, created = POProfile.objects.get_or_create(
            defaults={
                'first_name': profile_info['first_name'],
                'last_name': profile_info['last_name'],
                'email': profile_info['email']
            },
            first_name__iexact=profile_info['first_name'],
            last_name__iexact=profile_info['last_name'],
            email__iexact=profile_info['email'],
            phone_number=profile_info['phone_number'],
        )

        # Pass instance of 'po_profile' to create new 'PurchaseOrder' instance.
        purchase_order = serializer.save(po_profile=po_profile)

        # Set variables to send as kwargs to celery job.
        # Note: not required value or possible to be not provided will set as
        #       None.
        po_code = purchase_order.po_code

        promotion_title = check_res_data['cart_details'].get(
            'coupon_title', None
        )

        po_items = check_res_data['cart_details']['items']

        tax_title = None  # We aren't use any tax system right now.

        shipping = check_res_data['shipping_details']['shipping']
        shipping_details = {
            'method': check_res_data['shipping_details']['method'],
            'cost': check_res_data['shipping_details']['shipping_cost_amount'],
            'cost_currency':
                check_res_data['shipping_details']['price_currency'],
            'country_iso_code': shipping['country']['iso_code'],
            'address1': shipping['address_details']['address1'],
            'address2': shipping['address_details']['address2'],
            'city': shipping['address_details']['city'],
            'region': shipping['address_details']['region'],
            'postal_code': shipping['address_details']['postal_code']
        }

        # Since check response dones not return the all passed payment details,
        # so we get them from the request itself.
        payment_details = self.request.data["payment"]

        # Create url for specific view using reverse method.
        order_url = reverse(
            'order:specific-purchase-order-details-template',
            kwargs={'po_code': po_code}
        )

        # Create absolute url using current request object for order_url value.
        order_absolute_url = self.request.build_absolute_uri(order_url)

        # Trigger celery task to set purchase order details.
        set_purchase_order_details.delay(
            po_code=po_code,
            promotion_title=promotion_title,
            payment_details=payment_details,
            tax_title=tax_title,
            shipping_details=shipping_details,
            po_items=po_items,
            order_details_url=order_absolute_url
        )


class PurchaseOrderRetrieveTemplateAPIView(generics.RetrieveAPIView):
    """APIView to retrieve specific purchase order details in template"""

    # Specify the page to be rendered with TemplateView class.
    # Note: get_template or any other method of 'loader' module that implement
    #       in 'TemplateView' class will depend on 'DIRS' parameter of
    #       'TEMPLATES' list variable in 'settings.py' file for looking for the
    #       given template name.
    template_name = 'order/html/order-confirm.html'
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    serializer_class = serializers.PurchaseOrderDetailsSerializer
    queryset = PurchaseOrder.objects.all()
    # The default lookup_field is 'pk' and should be pass as argument in URL.
    lookup_field = 'po_code'
