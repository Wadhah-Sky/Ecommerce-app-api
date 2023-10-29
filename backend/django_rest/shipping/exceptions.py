from rest_framework.exceptions import APIException


class InvalidShippingMethod(APIException):
    # Bad request
    status_code = 400
    default_detail = "The given shipping method, it's not exist or not " \
                     "available anymore"
    default_code = "invalid_shipping_method_value"
