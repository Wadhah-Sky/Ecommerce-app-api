"""Define the serializers for you views"""

from rest_framework import serializers
# from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.conf import settings
from datetime import date

from core.models import POItem, PurchaseOrder, MetaItem, Address


def get_home_url():
    """Return the home url of frontend server"""

    try:
        # Get current 'Site' model instance from database.
        current_site = Site.objects.get_current()

        # Return 'domain' field value, which looks like:
        # http://127.0.0.1:8000/ or https://jamieandcassie.store

        # Note: if you are using nginx server for development or localhost,
        #       this will return the port of Django service not the nginx.
        return current_site.domain

    except ObjectDoesNotExist:
        return settings.MAIN_DOMAIN_NAME


class AddressSerializer(serializers.ModelSerializer):
    """Customized serializer class of Address model"""

    class Meta:
        """Serialize specific model fields"""

        model = Address
        fields = [
            'city',
            'region',
            'country_iso_code',
            'formatted_address'
        ]

    # Define related/reverse model fields.
    country_iso_code = serializers.SerializerMethodField()
    formatted_address = serializers.SerializerMethodField()

    def get_country_iso_code(self, instance):
        """Return object of country iso code for current instance"""

        if instance.country:
            return instance.country.iso_code

    def get_formatted_address(self, instance):
        """Return a formatted version of the address"""

        return {
            'line1': f'{instance.city}, {instance.region}',
            'line2': f'{str(self.get_country_iso_code(instance)).upper()}'
        }


class PurchaseOrderSerializer(serializers.ModelSerializer):
    """Customized serializer class of PurchaseOrder model"""

    # Note: For create View, the 'fields' list in Meta class of serializer is
    #       important to specify which field: value to return when create()
    #       and perform_create() methods done successfully.

    class Meta:
        """Serialize specific model fields"""

        model = PurchaseOrder
        fields = ['po_code', 'summary', 'status']
        read_only_fields = ['id', 'po_code', 'status']


class POItemSerializer(serializers.ModelSerializer):
    """Customized serializer class of POItem model"""

    class Meta:
        """Serialize specific model fields"""

        model = POItem
        fields = [
            'title',
            'sku',
            'quantity',
            'total_amount',
            'attributes',
            'thumbnail',
            'product_url'
        ]

    # Define related/reverse model fields.
    title = serializers.SerializerMethodField()
    sku = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
    product_url = serializers.SerializerMethodField()

    def get_title(self, instance):
        """Return the title for current instance"""

        return instance.product_item.product.title

    def get_sku(self, instance):
        """Return the sku for current instance"""

        return instance.product_item.sku

    def get_total_amount(self, instance):
        """Return the total amount property of instance"""

        return instance.total_amount

    def get_attributes(self, instance):
        """Return current instance attributes title as key: value (string)"""

        # Get the attribute instances of current instance's product item field.
        attributes = instance.product_item.attributes

        if attributes:

            # Initialize an empty dictionary
            returned_obj = {}

            for attr in attributes:

                # Get root attribute title.
                root_title = attr.get_root().title

                # In case 'root_title' doesn't exist as key yet.
                if returned_obj.get(root_title) is None:
                    returned_obj[root_title] = attr.title
                else:
                    # Append the attribute title into existing list of
                    # root_title key.
                    returned_obj[root_title] = f'{returned_obj[root_title]}' \
                                               f', {attr.title}'

            return returned_obj

    def get_thumbnail(self, instance):
        """Return the available thumbnail of the instance's product item"""

        if instance.product_item.available_thumbnail:

            # Get url of retrieved thumbnail file.
            url = instance.product_item.available_thumbnail.url

            # Note: here we return the available thumbnail, either the one that
            #       related to the instance's product item itself or the
            #       product parent instance, in this case Django can't
            #       serialize the thumbnail directly as absolute url we need to
            #       do manually.

            # Get request object from 'context'.
            # request = self.context.get("request", None)

            # if request:
            #
            #     return request.build_absolute_uri(url)
            #
            # else:
            #     # Get current 'Site' model instance from database.
            #     current_site = Site.objects.get_current()
            #
            #     # Use 'domain' field value with thumbnail url value to create
            #     # full path (absolute url) to thumbnail file.
            #     return current_site.domain + url

            return f'{get_home_url()}{url}'

    def get_product_url(self, instance):
        """Return the product item url of frontend server"""

        # Get request object from 'context'.
        request = self.context.get("request", None)

        # Get product slug for current product item
        product_slug = instance.product_item.product.slug

        # Get current product item slug
        instance_slug = instance.product_item.slug

        # Initialize frontend page route.
        url = f'/product/{product_slug}?itemS={instance_slug}'

        if request:
            return request.build_absolute_uri(url)
        else:
            return f'{get_home_url()}{url}'


class PurchaseOrderDetailsSerializer(serializers.ModelSerializer):
    """Customized serializer class of PurchaseOrder model"""

    # Note: Here in this class that is being implemented by view with template
    #       you will not need to worry about Money value and the following
    #       error while you should return amount/currency separately:
    #
    #       Objet value Money is not JSON serializer
    #
    #       because in the that view we use (TemplateHTMLRenderer) which render
    #       the response to:
    #
    #       (media_type = 'text/html') NOT (media_type = 'application/json')
    #
    #       even if you use both of them as 'renderer_classes'.

    class Meta:
        """Serialize specific model fields"""

        model = PurchaseOrder
        fields = [
            'po_code',
            'created_at',
            'po_profile',
            'po_shipping',
            'po_payment',
            'po_items',
            'shipping_address',
            'billing_address',
            'subtotal',
            'discount',
            'po_tax',
            'grand_total'
        ]

    # Define related/reverse model fields.
    created_at = serializers.SerializerMethodField()
    po_profile = serializers.SerializerMethodField()
    po_shipping = serializers.SerializerMethodField()
    po_payment = serializers.SerializerMethodField()
    po_items = serializers.SerializerMethodField()
    shipping_address = serializers.SerializerMethodField()
    billing_address = serializers.SerializerMethodField()

    @property
    def get_contact_url(self):
        """Return the contact us url of frontend server"""

        return f'{get_home_url()}/contact'

    @property
    def get_about_url(self):
        """Return the about us url of frontend server"""

        return f'{get_home_url()}/about'

    def get_order_details_url(self, instance):
        """Return the order details url of backend view template"""

        # Create url for specific view using reverse method.
        order_url = reverse(
            'order:specific-purchase-order-details-template',
            kwargs={'po_code': instance.po_code}
        )

        # Note: don't put back-slash between two values because order_url
        # start with back-slash.
        return f'{get_home_url()}{order_url}'

    def get_po_profile(self, instance):
        """Return the instance's po_profile details"""

        if instance.po_profile:
            return {
                'first_name': str(instance.po_profile.first_name).capitalize(),
                'last_name': str(instance.po_profile.last_name).capitalize()
            }

        return {
            'first_name': '',
            'last_name': ''
        }

    def get_created_at(self, instance):
        """Returns a string representing date using created_at field value"""

        # Return string of date value in (Month Day, Year) format.
        return instance.created_at.strftime('%B %d, %Y')

    def get_po_shipping(self, instance):
        """Return the instance's shipping details"""

        if instance.po_shipping:
            return {
                'title': instance.po_shipping.shipping_method.title,
                'cost': instance.shipping_cost
            }

        return {
            'title': '',
            'cost': 0.00
        }

    def get_po_payment(self, instance):
        """Return the instance's payment details"""

        if instance.po_payment:
            icon_instance = instance.po_payment.payment_method.icon

            return {
                'title': instance.po_payment.payment_method.title,
                'icon_src': icon_instance.source_url if icon_instance else '',
                'icon_src2':
                    icon_instance.source2_url if icon_instance else '',
                'card_number': instance.po_payment.scripted_card_number

            }

        return {
            'title': '',
            'icon_src': '',
            'card_number': ''
        }

    def get_po_items(self, instance):
        """Return the related serialized po_items for current instance"""

        po_items = instance.po_items_purchase_order.all()

        if po_items:
            return POItemSerializer(
                instance=po_items,
                many=True,
                read_only=True,
                context=self.context
            ).data

        return []

    def get_shipping_address(self, instance):
        """Return the related serialized address for current instance"""

        if instance.po_shipping:

            address = instance.po_shipping.address

            return AddressSerializer(
                instance=address,
                many=False,
                read_only=True
            ).data

        return {}

    def get_billing_address(self, instance):
        """Return the related serialized address for current instance's
        po_payment"""

        if instance.po_payment:

            address = instance.po_payment.address

            return AddressSerializer(
                instance=address,
                many=False,
                read_only=True
            ).data

        return {}

    def get_absolute_url(self, url):
        """Return the absolute url for given value"""

        if url:

            # Get request object from 'context'.
            request = self.context.get("request", None)

            if request:

                return request.build_absolute_uri(url)

            else:
                # Use 'domain' field value with given url value to create
                # full path (absolute url) to the given url.
                return f'{get_home_url()}{url}'

        return None

    def to_representation(self, instance):
        """Custom representation field to add to each returned instance"""

        # Note: this method DON'T require to declare the returned fields into
        # 'fields' list that defined in Meta class, and it's work similar to
        # SerializerMethodField() method.

        to_ret = super().to_representation(instance)

        # Get required data from database
        current_year = date.today().year
        meta_item = MetaItem.objects.filter(
            meta__title=settings.WEBSITE_MAIN_LOGO_TITLE
        ).first()

        # Initialize variables
        logo_thumbnail_url = None
        logo_svg_url = None

        # check if meta item is exists.
        if meta_item:
            # Check if your source for meta item is True:
            if meta_item.use_source:
                logo_svg_url = meta_item.source_url
                logo_thumbnail_url = meta_item.source2_url

            else:
                # Check if meta item has thumbnail
                if meta_item.thumbnail:
                    # logo_thumbnail_url = self.get_absolute_url(
                    #     meta_item.thumbnail.url
                    # )

                    logo_thumbnail_url = meta_item.thumbnail.url

                # Check if meta item has file
                if meta_item.file:
                    # logo_svg_url = self.get_absolute_url(meta_item.file.url)

                    logo_svg_url = meta_item.file.url

        # Set JSON keys value.
        to_ret['logo_thumbnail'] = f'{get_home_url()}{logo_thumbnail_url}'
        to_ret['logo_svg'] = f'{get_home_url()}{logo_svg_url}'
        to_ret['current_year'] = current_year
        to_ret['order_details_url'] = self.get_order_details_url(instance)
        to_ret['home_url'] = get_home_url()
        to_ret['contact_url'] = self.get_contact_url
        to_ret['about_url'] = self.get_about_url

        return to_ret
