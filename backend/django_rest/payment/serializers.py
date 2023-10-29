"""Define the serializers for you views"""

from rest_framework import serializers

from core.models import PaymentMethod


class PaymentMethodSerializers(serializers.ModelSerializer):
    """Serializer class of PaymentMethod model"""

    class Meta:
        """Serialize specific model fields"""

        model = PaymentMethod
        fields = [
            'label',
            'value',
            'is_card',
            'icon',
            'icon_color'
        ]

    # Define related/reverse model fields.
    label = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()

    def get_label(self, instance):
        """Method to return instance title"""

        return instance.title

    def get_value(self, instance):
        """Method to return instance title as lower case"""

        return instance.title

    def get_icon(self, instance):
        """Method to return instance icon 'class_attribute_value' """

        if instance.icon:
            return str(instance.icon.class_attribute_value).strip()
