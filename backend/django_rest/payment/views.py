"""Create your api Views"""

from rest_framework import generics, views, status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from core.models import match_with_regex, PaymentMethod
from core.views import AddressCheckAPIView, PersonalInfoCheckAPIView
from payment import serializers
from payment import exceptions

# import copy


class PaymentMethodListAPIView(generics.ListAPIView):
    """APIView to list all available payment method"""

    serializer_class = serializers.PaymentMethodSerializers
    queryset = PaymentMethod.objects.filter(
        is_available=True
    ).distinct().order_by('title')


class CardPaymentCheckAPIView(views.APIView):
    """APIView card payment check"""

    def post(self, request, data=None):
        """HTTP POST method"""

        # Data attribute value for this view POST method should be:
        # {
        #   "cardholder_name": <value>,
        #   "card_number": <value>,
        #   "card_expiry": <value>, # e.g, 12/24
        #   "card_ccv": <value> # should be either 3 or 4 digits
        #  }

        to_use = data if data else request.data

        # Get cardholder name.
        cardholder_name = to_use.get("cardholder_name", None)

        # Check cardholder name.
        if cardholder_name:

            # if regex matching return false.
            if not match_with_regex('cardholder_name', cardholder_name):
                return Response(
                    {
                        "message": "Invalid cardholder name",
                        "cardholder_name": cardholder_name
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"message": "Cardholder name is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get card number.
        card_number = to_use.get("card_number", None)

        # Check card number.
        if card_number:

            # if regex matching return false.
            if not match_with_regex('card_number', card_number):
                return Response(
                    {
                        "message": "Invalid card number",
                        "card_number": card_number
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"message": "Card number is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get card expiry
        card_expiry = to_use.get("card_expiry", None)

        # Check card expiry.
        if card_expiry:

            # if regex matching return false.
            if not match_with_regex('card_expiry', card_expiry):
                return Response(
                    {
                        "message": "Invalid card expiry",
                        "card_expiry": card_expiry
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"message": "Card expiry is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get card ccv
        card_ccv = to_use.get("card_ccv", None)

        # Check card ccv.
        if card_ccv:

            # if regex matching return false.
            if not match_with_regex('card_ccv', card_ccv):
                return Response(
                    {
                        "message": "Invalid card ccv",
                        "card_ccv": card_ccv
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"message": "Card ccv is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # If everything went ok
        return Response(
            {
                "cardholder_name": cardholder_name,
                "card_number": card_number,
                "card_expiry": card_expiry,
                "card_ccv": card_ccv
            },
            status=status.HTTP_200_OK
        )


class BillingAddressCheckAPIView(views.APIView):
    """APIView billing address check"""

    def post(self, request, data=None):
        """HTTP POST method"""

        # Data attribute value for this view POST method should be:
        # {
        #  "personal_info": {
        #              "first_name": <value>,
        #              "last_name": <value>,
        #              "phone_number": <value>
        #   },
        #  "country": { # possible, one of them
        #        "iso_code": <value>,
        #        "title": <value>
        #  },
        #  "address_details": {
        #              "address1": <value>,
        #              "address2": <value>,
        #              "region": <value>,
        #              "city": <value>,
        #              "postal_code": <value>
        #  }
        # }

        to_use = data if data else request.data

        personal_info = to_use.get("personal_info", None)

        if personal_info:

            # Check personal info.
            # Note: personal check require email value, but in billing address
            #       there is no email, so we set default value.
            personal_check_res = PersonalInfoCheckAPIView().post(
                request=request,
                data={
                    "first_name": personal_info["first_name"],
                    "last_name": personal_info["last_name"],
                    "email": "default@default.com",
                    "phone_number": personal_info["phone_number"]
                }
            )

            if personal_check_res.status_code != status.HTTP_200_OK:
                return Response(
                    personal_check_res.data,
                    status=personal_check_res.status_code
                )

            # In case personal info check went ok.
            country = to_use.get('country', None)
            address_details = to_use.get('address_details', None)

            address_check_res = AddressCheckAPIView().post(
                request=request,
                data={"country": country, "address_details": address_details}
            )

            if address_check_res.status_code != status.HTTP_200_OK:
                return Response(
                    address_check_res.data,
                    status=address_check_res.status_code
                )
        else:
            return Response(
                {
                    "message": "No personal info have provided"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # In case everything went ok.
        data_to_return = {}
        data_to_return.update(personal_check_res.data)
        data_to_return.update(address_check_res.data)

        return Response(data_to_return, status=status.HTTP_200_OK)


class PaymentCheckApiView(views.APIView):
    """APIView for payment check"""

    def post(self, request, data=None):
        """HTTP POST method"""

        # Data attribute value for this view POST method should be:
        # {
        #   "method": <value>, # the only thing required if payment method is
        #                      # not card.
        #   "card_details": {
        #       "holder_name": <value>,
        #       "number": <value>,
        #       "expiry": <value>, # e.g, 12/24
        #       "ccv": <value> # should be either 3 or 4 digits
        #
        #  },
        #  "use_shipping_address": <value>, # boolean, don't use quotes
        #  "billing": { # not required if 'use_shipping_address' is true
        #         "personal_info": {
        #                     "first_name": <value>,
        #                     "last_name": <value>,
        #                     "email": <value>,
        #                     "phone_number": <value>
        #          },
        #         "country": { # possible, one of them
        #                "iso_code": <value>,
        #                "title": <value>
        #          },
        #         "address_details": {
        #                       "address1": <value>,
        #                       "address2": <value>,
        #                       "region": <value>,
        #                       "city": <value>,
        #                       "postal_code": <value>
        #          }
        #  }
        # }

        to_use = data if data else request.data
        method = to_use.get('method', None)

        if method:

            try:
                instance = PaymentMethod.objects.get(
                    title=method,
                    is_available=True
                )

                # check if retrieved payment method instance is 'card'.
                if instance.is_card:

                    card_details = to_use.get('card_details', None)
                    use_shipping_address = to_use.get(
                        'use_shipping_address', True
                    )

                    if card_details:
                        card_check_res = CardPaymentCheckAPIView().post(
                            request=request,
                            data=card_details
                        )

                        if card_check_res.status_code != status.HTTP_200_OK:
                            return Response(
                                card_check_res.data,
                                status=card_check_res.status_code
                            )
                    else:
                        # In case card details is not provided for card payment
                        # method
                        return Response(
                            {
                                "message": "Card details (cardholder_name, "
                                           "card_number, card_expiry and "
                                           "card_ccv) is required"
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    # In case card check went ok.
                    # Note: in python boolean you should know that:
                    #       1- not None is True
                    #       2- bool(<any-string>) is True,
                    #          e.g. bool("false") is True
                    if not use_shipping_address:

                        # in case use shipping address is NOT true

                        # Check billing address details for card payment method

                        billing = to_use.get("billing", None)

                        if billing:
                            # Call for billing address check view.
                            billing_check_res = BillingAddressCheckAPIView(
                            ).post(request, data=billing)

                            if billing_check_res.status_code != \
                                    status.HTTP_200_OK:
                                return Response(
                                    billing_check_res.data,
                                    status=billing_check_res.status_code
                                )
                        else:
                            return Response(
                                {
                                    "message": "Card billing address details "
                                               "are required"
                                },
                                status=status.HTTP_400_BAD_REQUEST
                            )

            except ObjectDoesNotExist:
                return Response(
                    {
                        'message':
                            exceptions.InvalidPaymentMethod.default_detail,
                        'default_code':
                            exceptions.InvalidPaymentMethod.default_code,
                        'method': method
                    },
                    status=exceptions.InvalidPaymentMethod.status_code,
                )

            # In case everything is valid.
            return Response(
                {
                    "message": "Payment method details is valid",
                    "method": instance.title,
                    "is_card": instance.is_card
                },
                status=status.HTTP_200_OK
            )

        else:
            # In case payment method is None.
            return Response(
                {
                    "message": "Payment method is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
