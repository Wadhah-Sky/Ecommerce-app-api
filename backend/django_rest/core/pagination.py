from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PageNumberPaginationNoCount(PageNumberPagination):
    """Override get_paginated_response function of PageNumberPagination class
     to remove 'count' from Response"""

    # Specify page size.
    page_size = 12

    def get_paginated_response(self, data):
        """For performance reason we will exclude 'count' from HTTP response"""

        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
