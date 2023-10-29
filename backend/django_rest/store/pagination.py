from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination


# Info: Sometimes maybe you want to use offset pagination instead of page
#       number pagination, If you choose to allow variable (or user-defined)
#       number of results per page:
#
#       GET https://api.example.org/accounts/?limit=100&offset=400
#
#       instead of:
#
#       GET https://api.example.org/accounts/?page=4
#
#       * The 'limit' indicates the maximum number of items to return, and is
#         equivalent to the 'page_size' in page number pagination.
#       * The 'offset' indicates the starting position of the query in relation
#         to the complete set of unpaginated items.


class PageNumberPaginationWithCount(PageNumberPagination):
    """Pagination class"""

    page_size = 12

    def get_paginated_response(self, data):
        """Override the method return to add 'page_size' for HTTP response"""

        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page_size', self.page_size),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
        ]))


class PageNumberPaginationNoCount(PageNumberPagination):
    """Override get_paginated_response function of PageNumberPagination class
     to remove 'count' from Response"""

    page_size = 12

    def get_paginated_response(self, data):
        """For performance reason we will exclude 'count' from HTTP response"""

        return Response(OrderedDict([
            ('page_size', self.page_size),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class LimitPagination(MultipleModelLimitOffsetPagination):
    """Offset pagination class to be use in views that use multiple queryset"""

    default_limit = 12
