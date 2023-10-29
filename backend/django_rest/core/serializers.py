"""Define the serializers for you views"""

from rest_framework import serializers

from core.models import Address, POProfile


class AddressCheckSerializer(serializers.ModelSerializer):
    """Customized serializer class of Address model"""

    # Important: since this serializer class is using by APIView that
    #            implement post() method, then you should make sure which
    #            fields of model class are read_only or not, otherwise the
    #            fields will show on Web 'browsable API' of django rest
    #            framework and also can receive data by HTTP POST request.

    class Meta:
        """Serialize specific model fields"""

        model = Address
        fields = [
            'address1',
            'address2',
            'city',
            'region',
            'postal_code'
        ]

        # read_only_fields = [
        #     'address1',
        #     'address2',
        #     'city',
        #     'region',
        #     'postal_code'
        # ]


class ProfileCheckSerializer(serializers.ModelSerializer):
    """Customized serializer class of POProfile model"""

    # Important: since this serializer class is using by APIView that
    #            implement post() method, then you should make sure which
    #            fields of model class are read_only or not, otherwise the
    #            fields will show on Web 'browsable API' of django rest
    #            framework and also can receive data by HTTP POST request.

    class Meta:
        """Serialize specific model fields"""

        model = POProfile
        fields = ['first_name', 'last_name', 'email', 'phone_number']
