from rest_framework.exceptions import APIException


class InvalidCouponCode(APIException):
    # Bad request
    status_code = 400
    default_detail = "The given coupon code, it's not exist or not available" \
                     " anymore"
    default_code = "invalid_coupon_value"


class InvalidProductItemSku(APIException):
    # Bad request
    status_code = 400
    default_detail = "The given product item sku, it's not exist or not " \
                     "available anymore"
    default_code = "invalid_product_item_sku"


class InvalidCartCheckData(APIException):
    # Bad request
    status_code = 400
    default_detail = "No cart items or coupon code have provided"
    default_code = "invalid_cart_check_data"


class InvalidProductItemQuantity(APIException):
    # Bad request
    status_code = 400
    default_detail = "The requested product item quantity, it's not " \
                     "available or exceed the limit per order"
    default_code = "invalid_product_item_quantity"


class InvalidCouponForCart(APIException):
    # Bad request
    status_code = 400
    default_detail = "The given coupon code is not related to any of your " \
                     "cart items"
    default_code = "invalid_coupon_for_cart"
