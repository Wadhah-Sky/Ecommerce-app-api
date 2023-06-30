"""Create your api Views"""

from rest_framework import views, generics, status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings

from shipping import serializers, exceptions
from core.models import round_money, Country, ShippingMethod


class ShippingCountryListAPIView(generics.ListAPIView):
    """APIView to list all available countries to ship to it"""

    serializer_class = serializers.CountrySerializers
    queryset = Country.objects.filter(is_available=True).distinct().order_by(
        'display_order',
        'title'
    )


class ShippingMethodListAPIView(generics.ListAPIView):
    """APIView to list all available shipping methods to ship with"""

    serializer_class = serializers.ShippingMethodSerializers
    queryset = ShippingMethod.objects.filter(
        is_available=True
    ).distinct().order_by('title')


class ShippingCostAPIView(views.APIView):
    """APIView for calculate shipping cost"""

    # Get the default value for money decimal digits from 'api' settings.
    money_decimal_digits = settings.MONEY_DECIMAL_PLACES

    def post(self, request):
        """HTTP POST method"""

        # Data attribute value for this view POST method should be:
        # {
        #   "shipping_method": <value>,
        #   "shipping_address":
        #                {
        #                   "country_iso_code": <value>,
        #                   "region": <value>,
        #                   "city": <value>,
        #                   "postal_code": <value>
        #                 }
        # }
        #
        # Note: you can access this HTTP request body by calling 'request.body'

        # Get the 'shipping_method' and 'shipping_address' property value from
        # data of HTTP POST request.
        shipping_method = request.data.get('shipping_method', None)
        shipping_address = request.data.get('shipping_address', None)

        # Initialize some variables.
        country = None
        country_iso_code = None
        region = None
        city = None
        postal_code = None

        # Check if shipping address is not empty/zero/None
        if shipping_address:

            # Get certain keys value from the provided shipping address.
            country_iso_code = shipping_address.get('country_iso_code', None)
            region = shipping_address.get('region', None)
            city = shipping_address.get('city', None)
            postal_code = shipping_address.get('postal_code', None)

            # Check the country iso code if provided.
            if country_iso_code:

                try:
                    # Get the country instance using ignore case for string of
                    # provided country iso code.
                    country = Country.objects.get(
                        iso_code__icontains=country_iso_code,
                        is_available=True
                    )

                except ObjectDoesNotExist:
                    return Response(
                        {
                            'message':
                                exceptions.InvalidCountryIsoCode.
                                default_detail,
                            'default_code':
                                exceptions.InvalidCountryIsoCode.default_code,
                            'country_iso_code': country_iso_code
                        },
                        status=exceptions.InvalidCountryIsoCode.status_code,
                    )

            else:
                # In case the country iso code is None.
                return Response(
                    {
                        'message': "No country iso code has provided"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:
            # In case no shipping address has provided
            return Response(
                {
                    'message': "No shipping address has provided"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if shipping method is provided and not None/empty/zero.
        if shipping_method:

            try:
                # Get the shipping method instance.
                shipping_m = ShippingMethod.objects.get(
                    title__icontains=shipping_method
                )

            except ObjectDoesNotExist:
                return Response(
                    {
                        'message':
                            exceptions.InvalidShippingMethod.default_detail,
                        'default_code':
                            exceptions.InvalidShippingMethod.default_code,
                        'shipping_method': shipping_method
                    },
                    status=exceptions.InvalidShippingMethod.status_code,
                )

        # In case no shipping method has provided.
        else:
            return Response(
                {
                    'message': "No shipping method has provided"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # In this part of the code should make REST api call to shipping method
        # carrier with required details and get the cost value in the HTTP
        # response, But since our project is Demo, we will set default value
        # for shipping cost.

        shipping_cost_price = round_money(amount=0)

        return Response(
            {
                'country': country.title,
                'country_iso_code': country_iso_code,
                'shipping_method': shipping_m.title,
                'price_currency_symbol': settings.CURRENCY_SYMBOLS[
                    shipping_cost_price.currency.code
                ],
                'shipping_cost_amount': "{:.2f}".format(
                    round(
                        shipping_cost_price.amount,
                        self.money_decimal_digits
                    )
                )
            },
            status=status.HTTP_200_OK,
        )
