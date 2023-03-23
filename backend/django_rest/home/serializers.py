"""Define the serializers for your Homepage views"""

from rest_framework import serializers
# from rest_framework.response import Response

# from django.conf import settings

from core.models import (Card, Section, Banner, Product, ProductGroup,
                         ProductItem)


# Note: serializer class receive the queryset after filter class have done its
#       process (in case View using filter class).


# Note: the calling of serializer inside another one called 'Nested
#       relationships'.

# Info: If you directly called the serializer class and pass to it
#       instance/instances will respond with object of <SerializerClass_name>
#       type in case (many=False) OR 'ListSerializer' type in case (many=True).
#       if you tried to return this object with your SerializerMethodField()
#       an exception will raise, in case (many=True):
#
#       TypeError: Object of type 'ListSerializer' is not JSON serializable
#
#       OR in case (many=False)
#
#       Object of type <SerializerClass_name> is not JSON serializable
#
#       So you have to return the mention object as JSON object, and you can do
#       this by adding 'data' property to the returned response.


class BannerSerializer(serializers.ModelSerializer):
    """Serialize class for Banner model"""

    class Meta:
        """Serialize all model fields expect the excluded"""

        model = Banner
        fields = ['thumbnail', 'title', 'frontend_path']
        # fields = '__all__'
        # exclude = []
        # read_only_fields = []


class CardSerializer(serializers.ModelSerializer):
    """Serialize class for Card model"""

    class Meta:
        """Serialize all model fields expect the excluded"""

        model = Card
        fields = [
            'thumbnail',
            'title',
            'summary',
            'frontend_link_text',
            'category_slug'
        ]

    # Define related/reverse model fields.
    category_slug = serializers.SerializerMethodField()

    def get_category_slug(self, instance):
        """Return foreign key (category) slug value"""

        return instance.category.slug


class SectionSerializer(serializers.ModelSerializer):
    """Serialize class for Section model"""

    class Meta:
        """Serialize all specified model fields"""

        model = Section
        fields = [
            'title',
            'cards'
        ]

    # Define related/reverse model fields.
    cards = serializers.SerializerMethodField()

    def get_cards(self, instance):
        """Return all serialized cards those related to current section
         instance"""

        # Get all related Card instances that their category is active.
        cards = Card.objects.filter(
            section_cards_card__section=instance,
            category__is_active=True
        )

        # Return the Card instances as JSON serializer object.
        return CardSerializer(instance=cards, many=True, read_only=True).data


class ProductItemSerializer(serializers.ModelSerializer):
    """Serializer class of Product model"""

    class Meta:
        """Serialize specific model fields"""

        model = ProductItem
        fields = [
            'slug',
            'thumbnail',
            'price_currency_symbol',
            'list_price_amount',
            'deal_price_amount',
        ]

    # Define related/reverse model fields.
    thumbnail = serializers.SerializerMethodField()
    list_price_amount = serializers.SerializerMethodField()
    deal_price_amount = serializers.SerializerMethodField()

    def get_thumbnail(self, instance):
        """Return the thumbnail of instance if it's not exists return the
        product parent thumbnail"""

        # Get request object from 'context'.
        request = self.context.get("request")

        # You can't use hasattr(instance, 'thumbnail') because instance has
        # thumbnail field, but it could be blank.
        if not instance.thumbnail:
            # This happens in situation where the selected product item had
            # no thumbnail.
            thumbnail = request.build_absolute_uri(
                instance.product.thumbnail.url
            )

        else:
            # Set the selected product item thumbnail to thumbnail variable
            thumbnail = request.build_absolute_uri(
                instance.thumbnail.url
            )

        return thumbnail

    def get_list_price_amount(self, instance):
        """Return the amount value of list_price"""

        return instance.list_price.amount

    def get_deal_price_amount(self, instance):
        """Return the amount value of deal_price"""

        if instance.deal_price:
            return instance.deal_price.amount

    def to_representation(self, instance):
        """Custom representation field to add to each returned instance"""

        # Note: this method DON'T require to declare the returned fields into
        # 'fields' list that defined in Meta class, and it's work similar to
        # SerializerMethodField() method.

        to_ret = super().to_representation(instance)

        promo_title = instance.latest_deal_promotion_item_title
        promo_summary = instance.latest_deal_promotion_item_summary

        to_ret['promotion_title'] = promo_title
        to_ret['promotion_summary'] = promo_summary

        return to_ret


class ProductSerializer(serializers.ModelSerializer):
    """Serializer class of Product model"""

    class Meta:
        """Serialize specific model fields"""

        model = Product
        fields = [
            'title',
            'slug',
            'product_items_count',
            'product_item'
        ]

    # Define related/reverse model fields.
    # title = serializers.StringRelatedField()
    product_items_count = serializers.SerializerMethodField()
    product_item = serializers.SerializerMethodField()

    def get_product_items_count(self, instance):
        """Return the count of items for certain Product instance"""

        return len(instance.product_items_product.all())

    def get_product_item(self, instance):
        """Return the related product item depending on if 'attr' query string
        set or not"""

        # Get the dictionary of product selected item.
        product_selected_item = self.context.get(
            'product_selected_item',
            None
        )

        # Initialize instance variable.
        instance_var = None

        # Return the product item instance if this product 'pk' if found in the
        # dictionary, or return None (which means we will serialize the item of
        # current product instance.)
        if product_selected_item:
            instance_var = product_selected_item[instance.pk]

        item_instance = instance.item_instance(item=instance_var)

        # You can use Response class to return data or directly return
        # dictionary of data.
        return ProductItemSerializer(
            instance=item_instance,
            read_only=True,
            many=False,
            context=self.context
        ).data


class ProductGroupSerializer(serializers.ModelSerializer):
    """Serializer class of ProductGroup model"""

    class Meta:
        """Serialize all specified model fields"""

        model = ProductGroup
        fields = [
            'title',
            'products'
        ]

    # Define related/reverse model fields.
    products = serializers.SerializerMethodField()

    def get_products(self, instance):
        """Return all serialized products those related to current product
        group instance"""

        # Get all related Product instances those are available.
        products = Product.objects.filter(
            product_group=instance,
            is_available=True
        )

        # Pass the context of this serializer class to child serializer class.
        return ProductSerializer(
            instance=products,
            many=True,
            read_only=True,
            context=self.context
        ).data
