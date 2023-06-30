"""Create your api Views"""

from rest_framework import generics
from rest_framework.generics import get_object_or_404

from core.models import Product, ProductItem, Attribute, ProductAttribute

from product import serializers
from product import exceptions


class ProductRetrieveAPIView(generics.RetrieveAPIView):
    """APIView to retrieve specific product details"""

    # Important: if you set queryset on class level (without define
    #            get_queryset() method) and tried to use self.get_queryset()
    #            within the class methods, this will return all model instances
    #            without filtering.

    serializer_class = {
        'product_details': serializers.ProductDetailsSerializer,
        'product_item_details': serializers.ProductOnlyItemDetailsSerializer,
    }
    # The default lookup_field is 'pk' and should be pass as argument in URL.
    lookup_field = 'slug'

    def get_serializer_class(self):
        """Override the super class method of selecting the appropriate
        serializer class"""

        # Get the value from 'only_item' url query parameter.
        only_item = self.request.query_params.get('only_item', None)

        # Check that if only_item value is equal to 'true' after strip/lower it
        if (str(only_item).strip()).lower() == 'true':
            return self.serializer_class['product_item_details']

        return self.serializer_class['product_details']

    def get_queryset(self):
        """Return product for current request url"""

        kwarg_slug = self.kwargs.get('slug', None)

        # We set distinct() method to queryset because condition:
        # product_items_product__isnull
        # we cause to get response of the same product in count of product
        # items.
        return Product.objects.filter(
            slug=kwarg_slug,
            is_available=True,
            product_items_product__isnull=False
        ).distinct()

    @property
    def get_product_item(self):
        """Return the related product item depending on one of the following:
            1- item_s query string.
            2- attr query string.
            3- default product item for current queryset.
        """

        # Get product item slug from 'item_s' url query parameter.
        item_slug = self.request.query_params.get('item_s', None)

        # Remember: attr query is a string seperated by comma(,) for multiple
        #           values
        attr = self.request.query_params.get('attr', None)

        # Get the product instance of this retrieve view.
        # Note: we use first() method to change queryset list that will contain
        #       only one instance into just an instance.
        product = self.get_queryset().first()

        # Initialize a none object.
        instance = None

        if item_slug:
            instance = get_object_or_404(ProductItem, slug=item_slug)

        # In case no item slug has provided.
        elif attr:
            attr_set = set(item.strip() for item in attr.split(','))

            attributes = Attribute.objects.filter(title__in=attr_set)

            if attributes:

                # Loop over all product items.
                for item in product.product_items_product.all():

                    # Get title of current product item attributes.
                    titles = set(attr.title for attr in item.attributes)

                    #  If the same elements are present in the two sets then
                    #  they are considered equal and True is returned,
                    #  otherwise False is returned.
                    if titles == attr_set:
                        instance = item
                        break

        # In case neither of 'attr' or 'item_slug' has provided
        else:
            instance = product.item_instance()

        if instance:
            return instance
        else:
            raise exceptions.ProductHasNoItem

    def get_serializer_context(self):
        """Override the serializer context"""

        # Get current class instance serializer context
        context = super().get_serializer_context()

        # Update the serializer context.
        context.update(
            {
                'product_item': self.get_product_item
            }
        )

        return context


# class ProductRetrieveItemDetailsAPIView(generics.RetrieveAPIView):
#     """APIView to retrieve specific product item details given product slug
#     """
#
#     serializer_class = serializers.ProductDetailsSerializer
#     # The default lookup_field is 'pk' and should be pass as argument in URL.
#     lookup_field = 'slug'
#
#     def get_queryset(self):
#         """Return product for current request url"""
#
#         kwarg_slug = self.kwargs.get('slug', None)
#
#         # We set distinct() method to queryset because condition:
#         # product_items_product__isnull
#         # we cause to get response of the same product in count of product
#         # items.
#         return Product.objects.filter(
#             slug=kwarg_slug,
#             is_available=True,
#             product_items_product__isnull=False
#         ).distinct()
