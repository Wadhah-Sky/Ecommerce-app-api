from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination


class PageNumberPaginationWithCount(PageNumberPagination):
    """Pagination class"""

    page_size = 12

    def get_paginated_response(self, data):
        """We will add 'page_size' for HTTP response"""

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
