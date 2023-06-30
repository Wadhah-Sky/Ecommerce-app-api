"""Define the serializers for you views"""

from rest_framework import serializers

from core.models import Country, ShippingMethod


class CountrySerializers(serializers.ModelSerializer):
    """Serializer class of Country model"""

    class Meta:
        """Serialize specific model fields"""

        model = Country
        fields = ['label', 'value']

    # Define related/reverse model fields.
    label = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    def get_label(self, instance):
        """Method to return instance title as first letter capitalized"""

        return str(instance.title).capitalize()

    def get_value(self, instance):
        """Method to return instance iso code as lower case"""

        return str(instance.iso_code).lower()


class ShippingMethodSerializers(serializers.ModelSerializer):
    """Serializer class of ShippingMethod model"""

    class Meta:
        """Serialize specific model fields"""

        model = ShippingMethod
        fields = ['label', 'value']

    # Define related/reverse model fields.
    label = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    def get_label(self, instance):
        """Method to return instance title"""

        return instance.title

    def get_value(self, instance):
        """Method to return instance title as lower case"""

        return str(instance.title).lower()
