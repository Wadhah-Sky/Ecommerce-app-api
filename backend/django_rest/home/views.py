"""Register your api views"""

from drf_multiple_model.views import ObjectMultipleModelAPIView

from home import serializers
from core.models import Banner, TopBanner, Section, ProductGroup


# Info: if you want to make queryset filtering for list APIView/ViewSet:
#
#       1 - Filtering against the URL, for example inside get_queryset(self)
#           method:
#           >> username = self.kwargs['username']
#
#           url could be: http://example.com/api/purchases/<username_value>/
#
#       2- Filtering against query parameters, for example inside
#          get_queryset(self) method:
#          >> username = self.request.query_params.get('username')
#
#          url could be: http://example.com/api/purchases?username=value


# def product_name_filter(queryset, request, *args, **kwargs):
#     """Customized filter function to be use in querylist"""
#     product_name = request.query_params['product']
#     return queryset.filter(product_name=product_name)


class HomeListAPIView(ObjectMultipleModelAPIView):
    """APIView to combine multiple queryset with their serializers to list
      all images that are active & all active home Banners in the related
      model"""

    #     # Specify offset pagination.
    #     # pagination_class = pagination.LimitPagination
    #
    #     # NOTE: to use multiple querylist, follow the two ways that shown
    #     #       below.
    #     #
    #     # First way:
    #     #
    #     # QueryList of queryset with their serializer.
    #     # Note: set the customized filter function with related queryset if
    #     #       wanted.
    #     # querylist = [
    #     #     {
    #     #         'queryset': models.Department.objects.filter(
    #     #                                               is_active=True),
    #     #         'serializer_class': serializers.DepartmentSerializer
    #     #     },
    #     #     {
    #     #         'queryset': models.Product.objects.filter(
    #     #             is_available=True,
    #     #             offer__isnull=False
    #     #         ),
    #     #         'serializer_class': serializers.ProductSerializer,
    #     #         'filter_fn': product_name_filter
    #     #     },
    #     # ]
    #
    #     # Second way:
    #     #
    #     # def get_querylist(self):
    #     #     """Return querylist in addition to define fields for each query
    #              in case want to make filter request"""
    #     #
    #     #     # Filter fields per each queryset.
    #     #     # Note: you should use the filter field name with the related
    #     #     #       queryset within queryset filter method.
    #     #     # product_name = self.request.query_params['product'].replace(
    #     #     #     '-', ' '
    #     #     # )
    #     #
    #     #     # QueryList of queryset with their serializer.
    #     #     querylist = [
    #     #         {
    #     #           'queryset': models.Department.objects.filter(
    #     #                                          is_active=True),
    #     #           'serializer_class': serializers.DepartmentSerializer
    #     #         },
    #     #         {
    #     #             'queryset': models.Product.objects.filter(
    #     #                 is_available=True,
    #     #                 offer__isnull=False
    #     #             ),
    #     #             'serializer_class': serializers.ProductSerializer
    #     #         },
    #     #     ]
    #     #
    #     #     return querylist

    def get_querylist(self):
        """Return querylist"""

        # QueryList of queryset with their serializer.
        querylist = [
            # queryset with its serializer for banners.
            {
                'queryset': Banner.objects.filter(
                    is_active=True,
                    frontend_path__isnull=False
                ).order_by('display_order'),
                'serializer_class': serializers.BannerSerializer
            },
            # queryset with its serializer for active top banners.
            {
                'queryset': TopBanner.objects.filter(
                    is_active=True
                ).order_by('display_order'),
                'serializer_class': serializers.TopBannerSerializer
            },
            # queryset with its serializer for sections.
            {
                'queryset': Section.objects.filter(
                    is_active=True
                ).order_by('display_order'),
                'serializer_class': serializers.SectionSerializer
            },
            # queryset with its serializer for products groups sliders.
            {
                'queryset': ProductGroup.objects.filter(
                    is_active=True,
                    products_product_group__isnull=False
                ).distinct().order_by('display_order')[:3],
                'serializer_class': serializers.ProductGroupSerializer
            }
        ]

        return querylist
