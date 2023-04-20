from rest_framework.exceptions import APIException


class ProductHasNoItem(APIException):
    status_code = 400
    default_detail = "Can't find related item for current product"
    default_code = "product_has_no_item"
