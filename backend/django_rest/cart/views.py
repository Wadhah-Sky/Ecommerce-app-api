"""Create your api Views"""

from rest_framework import views, status
from rest_framework.response import Response
# from rest_framework.generics import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
# from django.utils import timezone
from django.conf import settings

from core.models import (calculate_discount_amount, round_money, ProductItem,
                         Promotion, PromotionItem)

from cart import exceptions, serializers


class CartCheckApiView(views.APIView):
    """APIView for cart check"""

    # Get the default value for money decimal digits from 'api' settings.
    money_decimal_digits = settings.MONEY_DECIMAL_PLACES

    # Define a variable represent the serializer we gonna use.
    serializer_class = serializers.CartCheckSerializer

    def get(self, request):
        """HTTP GET method"""

        # Remember: 'items_sku' query is a string seperated by comma(,) for
        #           multiple values
        items_sku = request.query_params.get('items_sku', None)

        # Get the max_length of Attribute.title
        sku_max_length = ProductItem.sku.field.max_length

        # If 'items_sku' is not None, convert its value into set value (no
        # duplicate) and ignore any sku value that its length more than
        # 'sku_max_length'
        if items_sku:
            sku_set = set(
                item.strip() for item in items_sku.split(',')
                if len(item.strip()) <= sku_max_length
            )

            # Get ProductItem instances.
            product_items = ProductItem.objects.filter(
                sku__in=sku_set,
                stock__gt=0,
                supplier__is_available=True,
                product__is_available=True
            )

            # Create context dictionary with request object.
            serializer_context = {'request': request}

            # Call the serializer class with related info and retrieve the
            # serialized data.
            serialized = self.serializer_class(
                instance=product_items,
                read_only=True,
                many=True,
                context=serializer_context,
            )

            # Return HTTP response of serialized object.
            return Response(serialized.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        """HTTP POST method"""

        # Data attribute value for this view POST method should be:
        # {
        #   "coupon": <value>,
        #   "cart": {
        #       "items": [
        #            {
        #              "sku": <value>,
        #              "quantity": <value>
        #             } ...
        #        ]
        #   }

        # Note: Don't use single quotes keys or value for json object, will
        #       show the following error in backend server:
        #
        #       1- for keys:
        #          "JSON parse error - Expecting property name enclosed in
        #          double quotes"
        #
        #       2- for values:
        #          "JSON parse error - Expecting value

        # Info: For returned prices, We do the same for frontend calculations:
        #
        #       1- Round values to certain decimal digits.
        #       2- Format the value of round() method to be two decimals, this
        #          is important in case the value was integer without decimals.

        # Get the 'coupon' and 'items' property value from data of HTTP POST
        # request.
        coupon = request.data.get('coupon', None)
        cart = request.data.get('cart', None)

        # Initialize some variables.
        promotion_instance = ''
        product_item_instances = []

        # Note: since total_price will deal with Money type, don't initialize
        #       it as string or integer, will cause to raise the following
        #       error when trying to do math operations on it:
        #
        #       'NotImplementedType' object has no attribute 'decimal_places'
        total_price = round_money(amount=0)
        total_discount_amount = 0

        # In case both of 'coupon' and 'cart' parameters in HTTP post
        # request is None.
        if coupon is None and cart is None:
            return Response(
                {
                    'message': exceptions.InvalidCartCheckData.default_detail,
                    'default_code':
                        exceptions.InvalidCartCheckData.default_code
                },
                status=exceptions.InvalidCartCheckData.status_code
            )

        # In case coupon is not None.
        if coupon:
            try:
                promotion_instance = Promotion.objects.get(
                    title=coupon,
                    promotion_type='Coupon',
                    is_available=True
                )

                # Check that the retrieved promotion instance is_active
                # property return True, otherwise raise the following exception
                if not promotion_instance.is_active:
                    raise ObjectDoesNotExist

            except ObjectDoesNotExist:
                return Response(
                    {
                        'message':
                            exceptions.InvalidCouponCode.default_detail,
                        'default_code':
                            exceptions.InvalidCouponCode.default_code,
                        'coupon': coupon
                    },
                    status=exceptions.InvalidCouponCode.status_code,
                )

        # In case cart has 'cart'.
        if cart:

            items = cart.get('items', None)

            # Check if items is not None.
            if items:

                # Loop over items.
                for item in items:

                    # Check if quantity of each item is set otherwise it's 1 by
                    # default
                    if item.get('quantity', None):
                        # Note: quantity value is string in json object we
                        # convert to integer in order to use with math
                        # operations.
                        quantity = int(item['quantity'])
                    else:
                        # Default value is 1.
                        quantity = 1

                    try:
                        # Get the ProductItem instance of given 'sku' and make
                        # sure that its available (in stock) and the
                        # 'is_available' field = true of 'product' and
                        # 'supplier' foreign keys.
                        instance = ProductItem.objects.get(
                            sku=item['sku'],
                            stock__gt=0,
                            supplier__is_available=True,
                            product__is_available=True
                        )

                        # Get the limit per order value for current ProductItem
                        # instance.
                        limit = instance.limit_per_order

                        # Check that the given or default quantity value is not
                        # exceed the limit or current ProductItem stock value.
                        if quantity > limit or quantity > instance.stock:

                            return Response(
                                {
                                    'message':
                                        exceptions.InvalidProductItemQuantity.
                                        default_detail,
                                    'default_code':
                                        exceptions.InvalidProductItemQuantity.
                                        default_code,
                                    'sku': item['sku'],
                                    'quantity': item['quantity']
                                },
                                status=exceptions.InvalidProductItemQuantity.
                                status_code
                            )

                    except ObjectDoesNotExist:
                        return Response(
                            {
                                'message':
                                    exceptions.InvalidProductItemSku.
                                    default_detail,
                                'default_code':
                                    exceptions.InvalidProductItemSku.
                                    default_code,
                                'sku': item['sku']
                            },
                            status=exceptions.InvalidProductItemSku.status_code
                        )

                    # If everything went right for current ProductItem instance
                    # add it product_item_instances list with the requested
                    # quantity.
                    product_item_instances.append(
                        {
                            'instance': instance,
                            'quantity': quantity
                        }
                    )

        else:
            # In case given coupon code is valid and cart is empty.
            return Response(
                {
                    "coupon_title": promotion_instance.title,
                    "coupon_summary": promotion_instance.summary,
                    "coupon_discount":
                        f'{promotion_instance.discount_percentage}%',
                    'cart': None
                },
                status=status.HTTP_200_OK
            )

        # In case given coupon code is valid and cart has items.
        if promotion_instance:
            # Loop over items of 'product_item_instances' list, each item is
            # dictionary.
            for item in product_item_instances:

                # Get instance value of current item dictionary.
                instance = item['instance']

                # Get the deal_price or list price for ProductItem instance.
                price = instance.deal_price or instance.list_price

                # Check if current instance is connect to the given promotion
                # instance.

                # Get the promotion item instance.
                promotion_item = PromotionItem.objects.filter(
                    promotion=promotion_instance,
                    product_item=instance
                ).first()

                # If promotion item instance is not None.
                if promotion_item:

                    # Get instance discount percentage.
                    inst_discount_per = promotion_instance.discount_percentage

                    # Get amount after discount for the price.
                    amount_after_discount = calculate_discount_amount(
                        amount=price.amount,
                        discount_percentage=inst_discount_per
                    )

                    # Find the discount amount:
                    # price amount minus amount after discount.
                    discount_amount = price.amount - amount_after_discount

                    # Add rounded money amount of 'discount amount' multiplied
                    # by the requested quantity value into
                    # 'total_discount_amount'.
                    total_discount_amount += round_money(
                        amount=discount_amount * item['quantity']
                    ).amount

                    # Add rounded money of 'amount after discount' multiplied
                    # by the requested quantity value into 'total_price' Money.
                    total_price += round_money(
                        amount=amount_after_discount * item['quantity']
                    )

                else:
                    # In case the current product item is not connect with the
                    # given promotion instance, just add its price * quantity
                    # into total price of cart.
                    total_price += round_money(
                        amount=price.amount * item['quantity']
                    )

            # Check that the promotion instance is used with at least one of
            # cart items.
            if total_discount_amount:

                # Return the JSON response.
                return Response(
                    {
                        "coupon_title": promotion_instance.title,
                        "coupon_summary": promotion_instance.summary,
                        "coupon_discount":
                            f'{promotion_instance.discount_percentage}%',
                        'price_currency': total_price.currency.code,
                        'price_currency_symbol': settings.CURRENCY_SYMBOLS[
                            total_price.currency.code
                        ],
                        'total_price_amount': "{:.2f}".format(
                            round(total_price.amount,
                                  self.money_decimal_digits)
                        ),
                        'total_discount_amount': "{:.2f}".format(
                            round(total_discount_amount,
                                  self.money_decimal_digits)
                        ),
                        'items': items
                    },
                    status=status.HTTP_200_OK
                )

            else:
                # In case the promotion instance is valid but not related with
                # any item in the cart.
                return Response(
                    {
                        'message':
                            exceptions.InvalidCouponForCart.default_detail,
                        'default_code':
                            exceptions.InvalidCouponForCart.default_code,
                        'coupon': coupon
                    },
                    status=exceptions.InvalidCouponForCart.status_code
                )

        else:
            # In case cart has items but no coupon has given, we just find
            # total price for all items with quantity.
            for item in product_item_instances:

                # Get instance value of current item dictionary.
                instance = item['instance']
                # Get the deal_price or list price for ProductItem instance.
                price = instance.deal_price or instance.list_price

                total_price += round_money(
                    amount=price.amount * item['quantity']
                )

            # Return the JSON response.
            return Response(
                {
                    'coupon_title': None,
                    'coupon_summary': None,
                    'price_currency': total_price.currency.code,
                    'price_currency_symbol': settings.CURRENCY_SYMBOLS[
                        total_price.currency.code
                    ],
                    'coupon_discount': "{:.2f}".format(0),
                    'total_price_amount': "{:.2f}".format(
                        round(total_price.amount, self.money_decimal_digits)
                    ),
                    'total_discount_amount': "{:.2f}".format(
                        round(total_discount_amount, self.money_decimal_digits)
                    ),
                    'items': items
                },
                status=status.HTTP_200_OK
            )
