"""Define the serializers for you views"""

from rest_framework import serializers
# from rest_framework.response import Response

from django.db.models import Subquery

from itertools import chain
# from operator import attrgetter

from home.serializers import ProductSerializer
from core.models import (Product, ProductItem, ProductAttribute, Supplier,
                         ProductItemAttribute)


class SupplierSerializer(serializers.ModelSerializer):
    """Serializer class of Supplier model"""

    class Meta:
        """Serialize specific model fields"""

        model = Supplier
        fields = ['uuid', 'is_available']


class ProductItemSerializer(serializers.ModelSerializer):
    """Serializer class of ProductItem model"""

    class Meta:
        """Serialize specific model fields"""

        model = ProductItem
        fields = [
            'sku',
            'slug',
            'thumbnail',
            'price_currency_symbol',
            'list_price_amount',
            'deal_price_amount',
            'supplier',
            'details',
            'attributes',
            'limit_per_order',
            'low_stock',
            'temporarily_not_available',
            'images'
        ]

    # Define related/reverse model fields.
    supplier = SupplierSerializer(read_only=True)
    thumbnail = serializers.SerializerMethodField()
    list_price_amount = serializers.SerializerMethodField()
    deal_price_amount = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()
    low_stock = serializers.SerializerMethodField()
    temporarily_not_available = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

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

    # def get_attributes(self, instance):
    #     """Return the instance related attributes"""
    #
    #     attributes = instance.attributes
    #
    #     # Initialize empty dictionary.
    #     attributes_dict = {}
    #
    #     # Loop over queryset.
    #     for item in attributes:
    #         # print("Title:", item.title)
    #         # Get the root node title of the item instance.
    #         root_title = item.get_root().title
    #
    #         # Check if root title is exists as key in the dictionary.
    #         if attributes_dict.get(root_title) is not None:
    #             # Append current title to root title list value.
    #             attributes_dict[root_title].append(item.title)
    #
    #         else:
    #             # Add current attribute title as list to root title as key.
    #             attributes_dict[root_title] = [item.title]
    #
    #     return attributes_dict

    def get_attributes(self, instance):
        """Return current instance attributes title"""

        # Get the attributes of current instance.
        attributes = instance.attributes

        if attributes:

            # Initialize an empty dictionary
            returned_obj = {}

            for attr in attributes:

                # Get root attribute title.
                root_title = attr.get_root().title

                # In case 'root_title' doesn't exist as key yet.
                if returned_obj.get(root_title) is None:
                    returned_obj[root_title] = [attr.title]
                else:
                    # Append the attribute title into existing list of
                    # root_title key.
                    returned_obj[root_title].append(attr.title)

            return returned_obj

    def get_low_stock(self, instance):
        """Return true if current product item stock is below 10"""

        if instance.stock <= 0:
            return None
        elif instance.stock < 10:
            return True
        else:
            return False

    def get_temporarily_not_available(self, instance):
        """Return true if current product item stock zero or less also in case
        the supplier is not available"""

        if instance.stock <= 0 or not instance.supplier.is_available:
            return True
        else:
            return False

    def get_images(self, instance):
        """Return all related images for current instance"""

        # Get request object from 'context'.
        request = self.context.get("request")

        # Initialize empty list to store images url.
        images_url = []

        if instance.images:

            for item in instance.images:
                # Append current image instance url to the list.
                images_url.append(request.build_absolute_uri(item.image.url))

            return images_url

        else:
            # if instance has no images, return the default thumbnail.
            images_url = [self.get_thumbnail(instance=instance)]

            return images_url

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


class ProductItemsSerializer(serializers.ModelSerializer):
    """Serializer class of ProductItem model"""

    class Meta:
        """Serialize specific model fields"""

        model = ProductItem
        fields = ['slug', 'attributes']

    # Define related/reverse model fields.
    attributes = serializers.SerializerMethodField()

    def get_product_item_attribute_thumbnail(self, instance, attribute):
        """Return the thumbnail of instance if it's exists"""

        # Get the related product item attribute.
        product_item_attr = ProductItemAttribute.objects.filter(
            product_item=instance,
            product_attribute__attribute=attribute
        ).first()

        # if queryset return an object.
        if product_item_attr:

            # Get request object from 'context'.
            request = self.context.get("request")

            # You can't use hasattr(instance, 'thumbnail') because instance has
            # thumbnail field, but it could be blank.
            if product_item_attr.thumbnail:
                # Set the selected product item attribute thumbnail to
                # thumbnail variable.
                thumbnail = request.build_absolute_uri(
                    product_item_attr.thumbnail.url
                )

                return thumbnail

    def get_attributes(self, instance):
        """Return dictionary of attributes for current ProductItem instance"""

        # Get attributes of current instance.
        queryset = instance.attributes

        # Initialize an empty dictionary
        attr_dict = {}

        for attr in queryset:

            # Get root attribute for current attribute
            root_attr = attr.get_root()
            # Get title of root attribute for current attribute instance.
            root_title = root_attr.title

            # In case 'root_title' doesn't exist as key yet.
            if attr_dict.get(root_title) is None:
                # 'root_title' key store list of related values.
                attr_dict[root_title] = [
                    {
                        "parent_attribute": attr.parent.title,
                        "child_attribute": attr.title,
                        "thumbnail": self.get_product_item_attribute_thumbnail(
                            instance=instance,
                            attribute=attr
                        )

                    }
                ]
            else:
                # Append new object for the exist list of attr_dict[root_title]
                attr_dict[root_title].append(
                    {
                        "parent_attribute": attr.parent.title,
                        "child_attribute": attr.title,
                        "thumbnail": self.get_product_item_attribute_thumbnail(
                            instance=instance,
                            attribute=attr
                        )
                    }
                )

        return attr_dict


class ProductDetailsSerializer(serializers.ModelSerializer):
    """Serialize class of Product category"""

    class Meta:
        """Serialize specific model fields"""

        model = Product
        fields = [
            'slug',
            'title',
            'summary',
            'details',
            'common_attributes',
            'related_product_items',
            'available_attributes_combination',
            'use_item_attribute_img',
            'use_item_attribute_color_shape',
            'selected_product_item',
            'related_products'
        ]

    # Define related/reverse model fields.
    common_attributes = serializers.SerializerMethodField()
    related_product_items = serializers.SerializerMethodField()
    available_attributes_combination = serializers.SerializerMethodField()
    selected_product_item = serializers.SerializerMethodField()
    related_products = serializers.SerializerMethodField()

    def get_common_attributes(self, instance):
        """Return the common attributes of current instance"""

        # Get list of ProductAttributes of current instance.
        queryset = instance.product_attributes_product.filter(
            is_common_attribute=True
        )

        # Initialize empty dictionary.
        attributes_dict = {}

        # Loop over queryset.
        for item in queryset:

            # Get the root node title of the item instance.
            root_title = item.attribute.get_root().title
            attributes_dict[root_title] = item.attribute.title

        return attributes_dict

    def get_related_product_items(self, instance):
        """Return the uncommon attributes of current instance"""

        # Get list of ProductItems of current instance.
        queryset = instance.product_items_product.all()

        return ProductItemsSerializer(
            instance=queryset,
            many=True,
            read_only=True,
            context=self.context
        ).data

    def get_related_attributes(self, instance, prod_attr):
        """Return related attributes of specific attribute overall product
        items for current product"""

        # Get list of ProductItems of current instance.
        product_items = instance.product_items_product.filter(
            product_item_attributes_product_item__product_attribute=prod_attr
        )

        # Initialize an empty dictionary.
        attributes_dict = {}

        # Loop over product items.
        for item in product_items:

            # Get attributes of current product items with exception to
            # attribute family of provide product attribute.
            attributes = item.attributes.exclude(
                tree_id=prod_attr.attribute.tree_id
            )

            # Loop over attributes.
            for attr in attributes:

                # Get title of current attribute root.
                attr_root_title = attr.get_root().title

                # Check if attributes dictionary has root title as key or not.
                if attributes_dict.get(attr_root_title) is None:
                    attributes_dict[attr_root_title] = [attr.title]
                elif attr.title not in attributes_dict[attr_root_title]:
                    # Append non-duplicate values for specified key.
                    attributes_dict[attr_root_title].append(attr.title)

        # Return dictionary where provided product attribute title as key,
        # while its value is attributes dictionary.
        return {prod_attr.attribute.title: attributes_dict}

    def get_available_attributes_combination(self, instance):
        """Return the available combination of product items attributes for
        current product"""

        # Get list of uncommon ProductAttributes for current instance.
        queryset = instance.product_attributes_product.filter(
            is_common_attribute=False,
            product_item_attributes_product_attribute__isnull=False
        ).distinct()

        # Initialize empty dictionary.
        attributes_dict = {}

        # Loop over queryset.
        for item in queryset:

            # Get root attribute of current product attribute.
            root_attr = item.attribute.get_root()

            # Get title if root attribute.
            root_title = root_attr.title

            # Check dictionary has specific key or not.
            if attributes_dict.get(root_title) is None:

                attributes_dict[root_title] = self.get_related_attributes(
                    instance=instance,
                    prod_attr=item
                )
            else:
                # In case the 'root_title' is already found as key, then update
                # its value.
                attributes_dict[root_title].update(
                    self.get_related_attributes(
                        instance=instance,
                        prod_attr=item
                    )
                )

        return attributes_dict

    def get_selected_product_item(self, instance):
        """Return serialization of related product item"""

        # Get the related product item.
        product_item = self.context.get('product_item', None)

        return ProductItemSerializer(
            instance=product_item,
            read_only=True,
            many=False,
            context=self.context
        ).data

    def get_related_products(self, instance):
        """Method to return 12 of related products for current product"""

        # Get related attribute instances.
        attributes = instance.attributes

        # Initialize an empty list.
        result = []

        # Get list of 12 (max) of the newest related products for current
        # instance with condition of same category and at least one of related
        # attributes.
        queryset = Product.objects.filter(
            category=instance.category,
            is_available=True,
            product_attributes_product__attribute__in=attributes,
            product_items_product__isnull=False
        ).exclude(pk=instance.pk).distinct().order_by('-created_at')[:12]

        # Get queryset length.
        query_length = len(queryset)

        # Check if length of queryset is less than 12.
        if query_length < 12:

            # Get the category root node for current product instance.
            root_node = instance.category.get_root()

            # Set list of pk from queryset product instances.
            pk_list = [item.pk for item in queryset]

            # add current product instance pk.
            pk_list.append(instance.pk)

            # Get extra queryset product instances in size of
            # (12 - queryset length)
            # where category is list of current product's root category family
            # and exclude the product instances these listed in 'pk_list'.
            extra_queryset = Product.objects.filter(
                category__in=Subquery(root_node.get_family().values('pk')),
                is_available=True,
                product_items_product__isnull=False
            ).exclude(pk__in=pk_list).distinct().order_by(
                '-created_at'
            )[:12-query_length]

            # Combine the two queryset.
            result = chain(queryset, extra_queryset)

            # In case wanted to sort the combined two queryset.
            # Note: no major deference between 'operator.attrgetter' and
            #      'getattr'
            # result = sorted(
            #     set(chain(queryset, extra_queryset)),
            #     key=attrgetter('created_at'),
            #     reverse=True
            # )

        # If result is empty, means the main queryset contains 12 of product
        # instances.
        if not result:
            # So set the main queryset value to 'result'.
            result = queryset

        # Serialize the instances of 'result'.
        return ProductSerializer(
            instance=result,
            read_only=True,
            many=True,
            context=self.context
        ).data


class ProductOnlyItemDetailsSerializer(serializers.ModelSerializer):
    """Serialize class of Product model for selected item only"""

    class Meta:
        """Serialize specific model fields"""

        model = Product
        fields = ['selected_product_item']

    # Define related/reverse model fields.
    selected_product_item = serializers.SerializerMethodField()

    def get_selected_product_item(self, instance):
        """Return serialization of related product item"""

        # Get the related product item.
        product_item = self.context.get('product_item', None)

        return ProductItemSerializer(
            instance=product_item,
            read_only=True,
            many=False,
            context=self.context
        ).data
