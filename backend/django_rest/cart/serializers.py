"""Define the serializers for you views"""

# from rest_framework import serializers

from product.serializers import ProductItemSerializer


class CartCheckSerializer(ProductItemSerializer):
    """Customized serializer class of Cart model"""

    # Important: since this serializer class is using by APIView that
    #            implement post() method, then you should make sure which
    #            fields of model class are read_only or not, otherwise the
    #            fields will show on Web 'browsable API' of django rest
    #            framework and also can receive data by HTTP POST request.

    class Meta(ProductItemSerializer.Meta):
        """Serialize specific model fields"""

        # If you want to add new field to the existing ones.
        # fields = ProductItemSerializer.Meta.fields+('detail_only_property',)

        fields = [
            'sku',
            'slug',
            'thumbnail',
            'price_currency_symbol',
            'list_price_amount',
            'deal_price_amount',
            'limit_per_order',
        ]
        read_only_fields = ['sku', 'slug', 'limit_per_order']
