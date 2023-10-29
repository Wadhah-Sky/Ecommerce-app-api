from rest_framework.exceptions import APIException


class InvalidPaymentMethod(APIException):
    # Bad request
    status_code = 400
    default_detail = "The given payment method, it's not exist or not " \
                     "available anymore"
    default_code = "invalid_payment_method_value"
