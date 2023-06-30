"""Create your api Views"""

from rest_framework import generics

from payment import serializers
from core.models import PaymentMethod


class PaymentMethodListAPIView(generics.ListAPIView):
    """APIView to list all available payment method"""

    serializer_class = serializers.PaymentMethodSerializers
    queryset = PaymentMethod.objects.filter(
        is_available=True
    ).distinct().order_by('title')
