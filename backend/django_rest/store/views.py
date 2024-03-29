"""Create your api Views"""

from rest_framework import generics
from rest_framework.generics import get_object_or_404
# from rest_framework.filters import SearchFilter, OrderingFilter

# from django_filters import rest_framework as rest_filters

from django.db.models import Subquery

from elasticsearch_dsl import Q

from core.models import (Category, Product, Attribute)
from core.documents import ProductItemDocument
from core.views import PaginatedElasticSearchListAPIView
from home.serializers import ProductSerializer, ProductSearchSerializer
from store import serializers, pagination, filters

import re


# Info: If you're using the Django REST framework BrowsableAPI, it'll call the
#       get_queryset() of ModelViewSet again in order to display the forms, The
#       second get_queryset call performed by renderers.BrowsableAPIRenderer.
#       In the real case, when your clients requests your API as format=json,
#       BrowsableAPIRenderer is not executed.

# Info: The dir() function returns all properties and methods of the specified
#       object, without the values.

# Important: if you are trying to do query on model that implement (MPTTModel)
#            then you should know that the returned object will be:
#
#            (TreeQuerySet)
#
#            So it's collection, you need to select one to use model's methods
#            with, like:
#
#            1- get_family()
#            2- get_children()
#
#            How to select one?
#
#            1- use <Class_name>.objects.get().get_family()
#               if only ever one class object that matches.
#            2- use <Class_name>.objects.filter().first().get_family()

# Info: if you want to make queryset filtering for list APIView/ViewSet:
#
#       1 - Filtering against the URL, for example inside get_queryset(self):
#           username = self.kwargs['username']
#
#           url could be: http://example.com/api/purchases/<username_value>/
#
#       2- Filtering against query parameters, for example inside
#          get_queryset(self):
#          username = self.request.query_params.get('username')
#
#          url could be: http://example.com/api/purchases?username=value

# Info: if you are using django-filter package to do filtering on your queryset
#       of APIView/ViewSet class, you may notice that view in django rest
#       framework web browsable page there is 'Filter' button that if you
#       click on will open a form box with the related available filtering
#       options (which you defined in the related filter class), so, if you
#       want to get the details that shown in the form box, you can do so by
#       calling 'django-filter.views' and retrieve the details from
#       object_filter(request, filter-class) function.


##########################################################################

# Search


class SearchAPIView(PaginatedElasticSearchListAPIView):
    """APIView to list all store's products depending on search query"""

    # Set required attributes value of inherit class.
    kwargs_query = 'query'
    model_class = Product
    filter_lookup = 'product_items_product__sku'
    filter_keyword = 'sku'
    filter_exclude_arg = 'is_available'
    filter_exclude_val = 'False'
    filter_order_by = '-created_at'
    serializer_class = ProductSearchSerializer
    document_class = ProductItemDocument
    pagination_class = pagination.PageNumberPaginationWithCount

    def get_serializer_context(self):
        """Override the serializer context"""

        # Get current class instance serializer context
        context = super().get_serializer_context()

        # Get value of search response.
        search_response = self.get_search_response()

        # Create list of filter_keyword string from search response.
        items_sku = [ele[self.filter_keyword] for ele in search_response]

        # Update the serializer context.
        context.update(
            {
                'items_sku': items_sku
            }
        )

        return context

    def generate_q_expression(self, query):
        """Override the abstract method of inherit class"""

        # Normalize the query string by removing every special character with
        # space.
        # Note: you can use r"\W+" regex for every special character.
        normalized_query = re.sub(r"\W+", " ", query)

        # Get normalized query string value and convert it into lower case and
        # split it into list depending on space.
        query_list = str(normalized_query).lower().split(" ")

        # Return Q() expression for elasticsearch.
        # return Q(
        #     # Set way of search.
        #     # Note: multi_match means whenever there is a match in the
        #     #       defined 'fields', return the document (row).
        #     'multi_match',
        #     # Set query string that the elasticsearch analyzer will work on
        #     # against the defined 'fields'.
        #     query=query,
        #     # Set fields of document (row) of Type (table) that can analyzer
        #     # look at.
        #     fields=['product_info'],
        #     # Set the 'Levenshtein distance' algorithm way of search to be
        #     # use.
        #     # Note: The fuzziness argument specifies that the results match
        #     #       with a maximum edit distance of 2. It should be noted
        #     #       that fuzziness should only be used with values of 1 and
        #     #       2, meaning a maximum of 2 edits between the query and
        #     #       a term in a document is allowed. Larger differences are
        #     #       far more expensive to compute efficiently and are not
        #     #       processed by Lucene (Levenshtein distance).
        #     fuzziness='auto'
        # )

        # return Q(
        #     # Set way of search.
        #     # Note: 'bool' used as boolean of provided [should, must,
        #     #       must_not, filter]
        #     'bool',
        #     # Note: 'must' means: The clause (query) must appear in matching
        #     #       documents. These clauses must match, like logical AND.
        #     #       While 'should' means: At least one of these clauses must
        #     #       match, like logical OR.
        #     must=[
        #         Q('match', product_info=query),
        #     ],
        #     # You can specify how many times at least should match (in case
        #     # use should)
        #     # minimum_should_match=1
        # )

        # Here we are using another way which write query as dictionary object.
        # Note: Q object accept only single query object and cannot accept
        #       parameters when passing in a dict.
        # return Q(
        #     {
        #         "bool": {
        #             "must": [
        #                 {
        #                     # match_phrase means search the given query
        #                     # string in specified field (all query string
        #                     # words should
        #                     # be found)
        #                     "match_phrase":
        #                         {
        #                             "product_item_info": {
        #                                 "query": query,
        #                             }
        #                         }
        #                 }
        #             ]
        #         }
        #     }
        # )

        # Note: since 'match_phrase' doesn't support 'fuzziness', instead we
        #       use 'span_near' with 'span_multi' which is allows you to wrap
        #       a multi term query (one of wildcard, fuzzy, prefix, range or
        #       regexp query) as a span query, so it can be nested.
        # Info: 'prefix_length' (Optional, integer) Number of beginning
        #       characters left unchanged when creating expansions. Defaults
        #       to 0.
        return Q(
            {
                "bool": {
                    "must": [
                        {
                            # span_near matches spans which are near one
                            # another. One can specify slop, the maximum number
                            # of intervening unmatched positions, as well as
                            # whether matches are required to be in-order. The
                            # span near query maps to Lucene SpanNearQuery
                            "span_near": {
                                "clauses": [
                                    {
                                        "span_multi": {
                                            "match": {
                                                "fuzzy": {
                                                    "product_item_info": {
                                                        "value": item,
                                                        "fuzziness": 2,
                                                        "prefix_length": 1
                                                    }
                                                }
                                            }
                                        }
                                    } for item in query_list
                                ],
                                "slop": 100,
                                "in_order": False
                            }
                        }
                    ]
                }
            }
        )


#########################################################################


class CategoryListAPIView(generics.ListAPIView):
    """APIView to list all store's root nodes categories"""

    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.root_nodes().filter(is_active=True).order_by(
        'display_order'
    )


class CategoryRetrieveAPIView(generics.RetrieveAPIView):
    """APIView to retrieve specific category details"""

    serializer_class = serializers.CategoryDetailsSerializer
    # The default lookup_field is 'pk' and should be pass as argument in URL.
    lookup_field = 'slug'
    queryset = Category.objects.filter(is_active=True).distinct()

    # def get_queryset(self):
    #     """Return a specific category instance"""
    #
    #     kwarg_slug = self.kwargs.get('slug')
    #
    #     # Return the related category children (one depth, we manage it
    #     # through the serializer)
    #     return Category.objects.filter(
    #         slug=kwarg_slug,
    #         is_active=True
    #     )


class AttributeListAPIView(generics.ListAPIView):
    """APIView to list all store's attribute depending on category"""

    serializer_class = serializers.AttributeSerializer

    @property
    def get_category(self):
        """Return category instance if exists or raise 404"""

        # Get category slug from url parameter (argument).
        kwarg_category_slug = self.kwargs.get('category_slug', None)

        # Get the wanted category model instance depending on its slug,
        # otherwise return 404 response.
        return get_object_or_404(
            Category,
            slug=kwarg_category_slug,
            is_active=True
        )

    @property
    def get_category_ancestors_pk(self):
        """Return category instance ancestors"""

        return self.get_category.get_ancestors(include_self=True).values('pk')

    def get_queryset(self):
        """Return root attributes that their leaf_nodes are connected to
         specific category and its ancestors"""

        # Get category ancestors pk list
        ancestors = self.get_category_ancestors_pk

        # Get the attribute instances these connected to specific category
        # group.
        # Note: We can't get attributes of level 0 (root) because we all family
        #       tree of categories including leaf nodes.
        attributes = Attribute.objects.filter(
            category_attributes_attribute__category__in=ancestors
        ).distinct().only('tree_id')

        # Return all nodes that have level=0 (root node) and tree_id is in the
        # retrieved attribute instances.
        return Attribute.objects.filter(
            level=0,
            tree_id__in=[ele.tree_id for ele in attributes]
        ).order_by('display_order')

    def get_serializer_context(self):
        """Override the serializer context"""

        # Get current class instance serializer context
        context = super(AttributeListAPIView, self).get_serializer_context()

        # Update the serializer context.
        context.update(
            {
                'category_ancestors': self.get_category_ancestors_pk
            }
        )

        return context


class ProductListAPIView(generics.ListAPIView):
    """APIView to list all store's products depending on category"""

    serializer_class = ProductSerializer
    pagination_class = pagination.PageNumberPaginationWithCount

    # Note: for simple filter/ordering you cause use 'SearchFilter' and
    #       'OrderingFilter' from 'rest_framework.filters' and add it in
    #       filter_backends list.
    # filter_backends = [SearchFilter, OrderingFilter]

    # Usually you set default ordering using order_by ORM method with the
    # queryset, but you can also set default ordering list.
    # ordering = ['created_at']

    # You can set the possible model's fields name that can order against it,
    # Be careful if you didn't set ordering_fields, by default will be possible
    # to order against all model fields even password!
    # ordering_fields = ['title']

    # You can set search fields to search within it.
    # search_fields = ['product_attributes_product__attribute__title']

    # In our API we are using 'django_filters' module.
    filter_backends = [filters.ProductBackendFilter]
    # Specify filter set class.
    filterset_class = filters.ProductFilter

    def get_queryset(self):
        """Return category's products for current request url"""

        kwarg_category_slug = self.kwargs.get('category_slug', None)

        # Get the wanted category model instance depending on its slug,
        # otherwise return 404 response.
        category = get_object_or_404(
            Category,
            slug=kwarg_category_slug,
            is_active=True
        )

        # Limiting a subquery to a single column (id) and search using (in)
        # lookup expression, the subquery returns the leaf nodes of
        # categories (including the current one in case itself is a leaf
        # node).
        return Product.objects.filter(
            category__in=Subquery(
                category.get_leafnodes(include_self=True).values('pk')
            ),
            is_available=True,
            product_items_product__isnull=False
        ).distinct().order_by('-created_at')

    @property
    def get_attribute_leaf_nodes(self):
        """Return list of attribute leaf node instances depending on 'attr'
        query string that passed within url"""

        # Important: since Product model implement 'Mptt' class, means the
        #            return list of instance is 'TreeQuerySet'.

        # Remember: attr query is a string seperated by comma(,) for multiple
        #           values
        attr = self.request.query_params.get('attr', None)

        # Get the max_length of Attribute.title
        title_max_length = Attribute.title.field.max_length

        # If attr is not None, convert its value into set value (no duplicate)
        # and ignore any attr value that its length more than
        # 'title_max_length'.
        if attr:
            titles_set = set(
                item.strip() for item in attr.split(',')
                if len(item.strip()) <= title_max_length
            )

            # Get all attribute instances that its title equivalent to
            # 'titles_set'.
            attributes = Attribute.objects.filter(
                title__in=titles_set,
            )

            # Initialize list to hold attribute leaf nodes 'pk'.
            leaf_nodes = []

            # Loop over 'TreeQuerySet' of attributes.
            for item in attributes:
                # Note: get_leafnodes() method returns list of attributes
                #       as Attribute instance not 'TreeQuerySet'.
                leaf_nodes += item.get_leafnodes(include_self=True).values(
                    'pk'
                )

            # Convert leaf_nodes (list of dict for 'pk') into set value
            # depending on 'pk' value.
            pk_set = set([leaf['pk'] for leaf in leaf_nodes])

            # Info: Maybe you will ask why we not return the leaf_nodes as it,
            #       this because leaf_nodes is list Attribute instances and in
            #       our api filtering and serializer we use lookup like 'in'
            #       with 'pk' field in filter() method, also we are return
            #       instances using Mptt class methods, and this won't work if
            #       the provided list is not 'TreeQuerySet' and you have to
            #       create list by loop over that list and provide the 'pk'.

            return Attribute.objects.filter(pk__in=pk_set).only(
                'pk', 'tree_id', 'title'
            )

    @property
    def get_attribute_titles_lists(self):
        """Return list of lists for attribute titles that passed in 'attr'
        query string where same attributes family fit in one list"""

        attributes = self.get_attribute_leaf_nodes

        if attributes:

            # Initialize a list variable for store lists of titles.
            titles = []

            # Initialize a list variable for items that we check.
            looped_instances = []

            # Loop over attributes.
            for obj in attributes:

                # Check if the current obj title already picked up and checked.
                if not (obj.pk in looped_instances):

                    # Get list of attribute instances (only title) that tree_id
                    # is obj.tree_id and pk is (in) provided attributes.
                    instances = Attribute.objects.filter(
                        tree_id=obj.tree_id, pk__in=attributes
                    ).only('title')

                    # Check if instances is not empty list.
                    if instances:
                        # Loop over instances and extract title value and add
                        # as list of titles (surround [] of for loop with
                        # outside []).
                        titles += [[ele.title for ele in instances]]

                        # Add each obj pk of instances into looped_instances
                        for item in instances:
                            looped_instances.append(item.pk)

            return titles

    @property
    def get_selected_items_dict(self):
        """filter the passed attribute instances within 'attr' query string to
        be only related to product items"""

        # Check if 'attr' query string is set.
        if self.get_attribute_leaf_nodes:

            # From attributes those set, check if any of them have
            # 'is_common_attribute=False' (means attributes for product item
            # instances).
            product_item_attributes = self.get_attribute_leaf_nodes.filter(
                product_attributes_attribute__is_common_attribute=False
            ).distinct()

            # Check if there are product_item_attributes available.
            if product_item_attributes:

                # Create dictionary variable that store multiple keys in
                # format:
                #
                # {'product_pk': 'item_instance'}
                #
                selected_items_dict = {}

                # Get instances of view queryset.
                product_instances = self.get_queryset()

                # Loop over 'product_instances'.
                for product in product_instances:

                    # Initialize dictionary variable to store specific info.
                    dict_var = {'item': None, 'length': 0}

                    # Get product items of current product instance.
                    product_items = product.product_items_product.all()

                    # Loop over 'product_items'.
                    for item in product_items:

                        # Get item attributes these are same as the ones these
                        # passed within 'attr' query string.
                        attributes = item.attributes.filter(
                            pk__in=product_item_attributes
                        )

                        # Check if current length of attribute instances is
                        # bigger than current stored value in
                        # dict_var['length'].
                        if len(attributes) > dict_var['length']:
                            # Update the dict_var with new data.
                            dict_var = {
                                'item': item,
                                'length': len(attributes)
                            }

                    # Check if there is 'item' in dict_var.
                    if dict_var['item']:
                        # Set this item 'pk' to current product 'pk'.
                        selected_items_dict[product.pk] = dict_var['item']

                # Return the dictionary.
                return selected_items_dict

    def get_serializer_context(self):
        """Override the serializer context"""

        # Get current class instance serializer context
        # Note: in the latest versions of python, you don't need to set class
        #       name inside super() method.
        context = super().get_serializer_context()

        # Update the serializer context.
        context.update(
            {
                'selected_items_dict': self.get_selected_items_dict
            }
        )

        return context

    def get_filterset_kwargs(self):
        """Override filter backend 'filterset_kwargs' with new data to pass
        to the backend class"""

        titles = self.get_attribute_titles_lists

        return {
            'titles': titles,
            'selected_items_dict': self.get_selected_items_dict
        }
