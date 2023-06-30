"""Create your api Views"""

from rest_framework import views, status
from rest_framework.response import Response
# from rest_framework.decorators import api_view, parser_classes

from cart.views import CartCheckApiView
from shipping.views import ShippingCostAPIView

# from django.conf import settings
# from rest_framework.settings import api_settings
# from rest_framework.exceptions import ParseError
# from rest_framework import renderers
# from rest_framework.parsers import BaseParser
# from rest_framework.utils import json
# import codecs

import logging
# import requests


# Important: you should know that 'HttpRequest' AKA 'request._request' can't be
#            used multiple times after it has been read by Django Rest
#            Framework 'View' parser class that will lead to call 'read()'
#            method which will change the '_request' object's property
#            '_read_started' to be 'True', and after that if you tried to use
#            'request.data' or 'request._request' will raise the exception:
#
#            RawPostDataException: You cannot access body after reading from
#                                  request's data stream
#
#            Because the 'request.body' is not accessible anymore due it counts
#            on the value of '_read_started' property, also not to mention that
#            the value of 'HttpRequest' has already been converted into
#            'stream' object and stored in the memory, so if you are going to
#            use the below code to call another 'APIView' from another
#            'APIView' will lead to such case:
#
#            from rest_framework import views
#            from rest_framework.response import Response
#
#            from A.views import A
#
#            class B(views.APIView):
#
#                def post(self, request, *args, **kwargs):
#
#                     # Note: as_view() method can automatically specify the
#                     #       HTTP method to use for calling view class as same
#                     #       current request method.
#                     http_response = A.as_view()(request._request)
#
#                     # So far so good, but if I want to access request.data
#                     # after calling A.as_view() will raise the exception.
#
#                     return Response(http_response.data)
#
#
#            There are multiple suggestions I found:
#            1- use Middleware to store the request.body to use it later in
#               case of need.
#            2- use a custom parser class that store raw data as property in
#               request object before converting it into stream object.
#
#            Both of them I found is a little bit complicated, so I changed the
#            way of calling another 'APIView' from certain DRF 'View', as
#            shown:
#
#            # Initialize a new instance of class view 'A'
#            a_view = A()
#
#            # Calling HTTP 'POST' method with DRF request object.
#            a_http_response = a_view.post(request)


# class BodySavingJSONParser(BaseParser):
#     """
#     Custom parser of JSON-serialized data.
#     """
#
#     # Info: parser is the one who convert raw HTTP request passed data into
#     #       accessible data while render is responsible for converting
#     #       serialized data to raw data that transfer back to as response.
#
#     # Note: you can't get value of added 'raw_value' property unless the
#     #       parser is called, and usually it's called when trying to get
#     #       value of 'request.data'.
#
#     media_type = 'application/json'
#     renderer_class = renderers.JSONRenderer
#     strict = api_settings.STRICT_JSON
#
#     def parse(self, stream, media_type=None, parser_context=None):
#         """
#         Parses the incoming bytestream as JSON and returns the resulting data
#         """
#         parser_context = parser_context or {}
#         encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)
#         request = parser_context.get('request')
#
#         try:
#             decoded_stream = codecs.getreader(encoding)(stream)
#             decoded_content = decoded_stream.read()
#             # Saving decoded request original body to raw_body
#             setattr(request, 'raw_body', decoded_content)
#             parse_constant = json.strict_constant if self.strict else None
#             return json.loads(decoded_content, parse_constant=parse_constant)
#         except ValueError as exc:
#             raise ParseError('JSON parse error - %s' % str(exc))


class OrderAPIView(views.APIView):
    """APIView for order"""

    # Specify the parser to be use in your view. DRF view default parsers are:
    # 1- JSONParser()
    # 2- FormParser()
    # 3- MultiPartParser()

    # parser_classes = [BodySavingJSONParser]

    def get_cart_check(self, request):
        """Method to trigger HTTP request for cart api"""

        # cart_view = CartCheckApiView()
        cart_http_response = CartCheckApiView().post(request)

        return cart_http_response

    def get_shipping_cost(self, request):
        """Method to trigger HTTP request to shipping api"""

        # shipping_view = ShippingCostAPIView()
        shipping_http_response = ShippingCostAPIView().post(request)

        return shipping_http_response

    def post(self, request):
        """HTTP POST method"""

        try:

            # First step check cart items by calling /cart/check/ with HTTP
            # post request.

            cart_res = self.get_cart_check(request=request)

            if cart_res.status_code == status.HTTP_200_OK:

                # Second step:
                # 1- check shipping cost and
                # 2- check the requested shipping method and
                # 3- validate the shipping address by calling /shipping/cost/
                #    with HTTP post request.
                # 4- Get the shipping cost.

                shipping_res = self.get_shipping_cost(request=request)

                if shipping_res.status_code == status.HTTP_200_OK:

                    country = shipping_res.data['country']
                    country_iso_code = shipping_res.data['country_iso_code']
                    shipping_method = shipping_res.data['shipping_method']
                    currency_symbol = \
                        shipping_res.data['price_currency_symbol']
                    shipping_cost_amount = \
                        shipping_res.data['shipping_cost_amount']

                    # Note: so far we don't have tax system, so we will ignore

                else:
                    return Response(shipping_res.data)

            else:
                return Response(cart_res.data)

        except Exception as e:
            logging.exception(e)

            return Response(
                {
                    'message': "Error is occurred while trying to create the "
                               "order"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
