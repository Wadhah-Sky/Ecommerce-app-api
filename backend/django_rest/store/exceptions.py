from rest_framework.exceptions import APIException


class InvalidAttrValue(APIException):
    status_code = 400
    default_detail = "Single attribute value should consists no more than 25" \
                     " characters"
    default_code = "invalid_attr_value"


class InvalidPriceValueDataType(APIException):
    status_code = 400
    default_detail = "Price value should be a number"
    default_code = "invalid_price_data_type"


class InvalidMinPriceValue(APIException):
    status_code = 400
    default_detail = "Min price value should be between ($0 - $4999)"
    default_code = "invalid_min_price"


class InvalidMaxPriceValue(APIException):
    status_code = 400
    default_detail = "Max price value should be between ($1 - $5000)"
    default_code = "invalid_max_price"


class InvalidMinMaxPriceValue(APIException):
    status_code = 400
    default_detail = "Max price value should be bigger than min price value"
    default_code = "invalid_min_max_price"
