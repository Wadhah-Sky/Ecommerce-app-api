"""Create your api Views"""

from rest_framework import views, generics, status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings

from shipping import serializers, exceptions
from core.models import round_money, Country, ShippingMethod
from core.views import AddressCheckAPIView, PersonalInfoCheckAPIView


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

    def post(self, request, data=None):
        """HTTP POST method"""

        # Data attribute value for this view POST method should be:
        # {
        #   "method": <value>,
        #   "country": { # possible, one of them
        #         "iso_code": <value>,
        #         "title": <value>
        #    },
        #   "address_details": {
        #                 "address1": <value>, # Not required for check
        #                                      # due we set default value
        #                 "address2": <value>, # Not required
        #                 "region": <value>,
        #                 "city": <value>,
        #                 "postal_code": <value> # not required
        #   }
        #  }
        #
        # Note: you can access this HTTP request body by calling 'request.body'
        #       But it's not recommended in DRF.

        to_use = data if data else request.data

        # Get the 'method' and 'shipping' property value.
        method = to_use.get('method', None)
        country = to_use.get('country', None)
        address_details = to_use.get('address_details', None)

        address_check_res = {}

        # Check if shipping method is not empty/zero/None
        if method:

            if country and address_details:

                # Get certain keys value from the provided address details.
                address1 = address_details.get('address1', 'default')
                address2 = address_details.get('address2', 'default')
                region = address_details.get('region', None)
                city = address_details.get('city', None)
                postal_code = address_details.get('postal_code', "default")

                # Get certain keys value from the provided country.
                iso_code = country.get('iso_code', None)
                title = country.get('title', None)

                # Since post() method of 'CountryCheckAPIView' is access
                # directly to 'country_iso_code', so you need to pass it
                # through 'request' object But keep in mind the below line will
                # not copy the request object:
                #
                # address_check_req = request
                #
                # But you can copy the 'data' dictionary object:
                #
                # post = request.POST.copy()
                #
                # OR use deepcopy() method:
                #
                # post = copy.deepcopy(request.data)
                #
                # Note: by default GET/POST data is immutable

                # Since 'data' attribute has no setter, so we can't do:
                # country_check_req.data = {'iso_code': iso_code}
                #
                # we do the below to set required property value:

                # request.data.update(
                #     {
                #         "country": {
                #             "iso_code": country_iso_code
                #         },
                #         "address_details": {
                #             "address1": address1,
                #             "city": city,
                #             "region": region,
                #             "postal_code": postal_code
                #         }
                #     }
                # )

                address_check_data = {
                    "country": {
                        "iso_code": iso_code,
                        "title": title
                    },
                    "address_details": {
                        "address1": address1,
                        "address2": address2,
                        "city": city,
                        "region": region,
                        "postal_code": postal_code
                    }
                }

                # Call for address check view.
                address_check_res = AddressCheckAPIView().post(
                    request=request,
                    data=address_check_data
                )

                if address_check_res.status_code != status.HTTP_200_OK:
                    return Response(
                        address_check_res.data,
                        status=address_check_res.status_code
                    )
            else:
                if address_details is None:
                    # In case no address details have provided
                    return Response(
                        {
                            'message': "No address details have provided"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if country is None:
                    # In case no country details have provided
                    return Response(
                        {
                            'message': "No country title or iso code has "
                                       "provided"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        else:
            # In case no shipping address has provided
            return Response(
                {
                    'message': "No shipping details have provided"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if shipping method is provided and not None/empty/zero.
        if method:

            try:
                # Get the shipping method instance.
                shipping_m = ShippingMethod.objects.get(
                    title=method,
                    is_available=True
                )

            except ObjectDoesNotExist:
                return Response(
                    {
                        'message':
                            exceptions.InvalidShippingMethod.default_detail,
                        'default_code':
                            exceptions.InvalidShippingMethod.default_code,
                        'shipping_method': method
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

        ######################################################################
        # In this part of the code should make REST api call to shipping method
        # carrier api with required details and get the cost value in the HTTP
        # response, But since our project is Demo, we will set default value
        # for shipping cost.
        ######################################################################

        cost_price = round_money(amount=0)
        # Note: since 'data' of 'country_check_res' is JSON object, then don't
        #       call its parameters like you do with dictionary object in
        #       python.
        return Response(
            {
                'method': shipping_m.title,
                'shipping': {
                    'country': address_check_res.data.get('country', None),
                    'address_details': {
                        'address1': address_details.get('address1', ''),
                        'address2': address_details.get('address2', ''),
                        'city': address_check_res.data['address_details'].get(
                            'city', ''
                        ),
                        'region':
                            address_check_res.data['address_details'].get(
                                'region', ''
                            ),
                        'postal_code': address_details.get('postal_code', '')
                    },
                },
                'price_currency': cost_price.currency.code,
                'price_currency_symbol':
                    settings.CURRENCY_SYMBOLS[cost_price.currency.code],
                'shipping_cost_amount':
                    "{:.2f}".format(
                        round(cost_price.amount, self.money_decimal_digits)
                    )
            },
            status=status.HTTP_200_OK,
        )


class ShippingCheckAPIView(views.APIView):
    """APIView for shipping check"""

    def post(self, request, data=None):
        """HTTP POST method"""

        # Data attribute value for this view POST method should be:
        #
        # {
        #  "method": <value>,
        #  "personal_info": {
        #               "first_name": <value>,
        #               "last_name": <value>,
        #               "email": <value>,
        #               "phone_number": <value>
        #   },
        #  "country": { # possible, one of them
        #         "iso_code": <value>,
        #         "title": <value>
        #   },
        #  "address_details": {
        #                "address1": <value>, # Not required for check
        #                "address2": <value>, # Not required
        #                "region": <value>,
        #                "city": <value>,
        #                "postal_code": <value> # not required
        #  }
        # }

        to_use = data if data else request.data
        personal_info = to_use.get('personal_info', None)
        method = to_use.get('method', None)
        country = to_use.get('country', None)
        address_details = to_use.get('address_details', None)

        if personal_info:
            personal_info_check_res = PersonalInfoCheckAPIView().post(
                request=request,
                data=personal_info
            )

            if personal_info_check_res.status_code != status.HTTP_200_OK:
                return Response(
                    personal_info_check_res.data,
                    status=personal_info_check_res.status_code
                )

            # In case personal info check went with no issue.
            # Set data for shipping cost view.
            shipping_cost_data = {
                "method": method,
                "country": country,
                "address_details": address_details
            }

            shipping_cost_res = ShippingCostAPIView().post(
                request=request,
                data=shipping_cost_data
            )

            if shipping_cost_res.status_code != status.HTTP_200_OK:
                return Response(
                    shipping_cost_res.data,
                    status=shipping_cost_res.status_code
                )

            data_to_return = {}
            data_to_return.update(personal_info_check_res.data)
            data_to_return.update(shipping_cost_res.data)
            # In case everything went ok
            return Response(data_to_return, status=status.HTTP_200_OK)

        # In case personal info is None
        return Response(
            {
                "message": "No personal info have provided"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
