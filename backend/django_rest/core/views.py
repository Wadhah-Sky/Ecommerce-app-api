"""Register the views for this backend"""

from rest_framework import views, generics, status
from rest_framework.response import Response
# from rest_framework.parsers import JSONParser
from django.views.generic.base import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.http import (HttpResponseNotFound, HttpResponseForbidden,
                         HttpResponseServerError)
from django.db.models import Subquery

from dal import autocomplete

from core.models import Category, Attribute, ProductAttribute, Country
from core import exceptions
from core import serializers
from core import pagination

import abc
import logging


########################################################################

# Templates


class IndexTemplateView(TemplateView):
    """View class to render index.html template"""

    # Specify the page to be rendered with TemplateView class.
    # Note: get_template or any other method of 'loader' module that implement
    #       in 'TemplateView' class will depend on 'DIRS' parameter of
    #       'TEMPLATES' list variable in 'settings.py' file for looking for the
    #       given template name.
    template_name = 'index.html'


#######################################################################

# Autocomplete

class AttributeAutocompleteView(autocomplete.Select2QuerySetView):
    """Select2 autocomplete view class to return queryset for attribute
    field"""

    def get_queryset(self):
        """Customize the queryset for this class view"""

        # Note: Don't forget to filter out results depending on the requester!

        # Make sure the HTTP request is made by authenticated user, if
        # unauthenticated, then return nothing.
        if not self.request.user.is_authenticated:
            return HttpResponseForbidden('User is not authenticated')

        # Get the forwarded object id of 'category'.
        forwarded_category = self.forwarded.get('category', None)
        forwarded_product = self.forwarded.get('product', None)
        forwarded_is_common_attribute = self.forwarded.get(
            'is_common_attribute', True
        )

        try:
            # Get the category model instance.
            if forwarded_category:
                category = Category.objects.get(pk=forwarded_category)
            else:
                raise Exception('No category pk provided')
        except ObjectDoesNotExist:
            return HttpResponseNotFound('Category not found')
        except Exception as e:
            logging.exception(e)
            return HttpResponseServerError(
                'Error is occurred while trying to retrieve category'
            )
        else:
            try:
                if forwarded_is_common_attribute:
                    # Means we are trying to filter for ProductAttribute.

                    # Get Attribute model instances for specific category
                    # family (ancestors) including the current category model
                    # instance.
                    # Note: we need only leaf_nodes, so we will use the
                    #       related_name of 'parent' field to get only
                    #       instances these not have any leaf_nodes.
                    queryset = Attribute.objects.filter(
                        category_attributes_attribute__category__in=Subquery(
                            category.get_ancestors(include_self=True).values(
                                'pk'
                            )
                        ),
                        leaf_nodes__isnull=True
                    ).order_by('pk')

                else:
                    # Means we are trying to filter for ProductItemAttribute
                    queryset = ProductAttribute.objects.filter(
                        product=forwarded_product,
                        is_common_attribute=False
                    )

            except Exception as e:
                logging.exception(e)
                return HttpResponseServerError(
                    'Error is occurred while trying to retrieve attributes'
                )
            else:
                return queryset


#######################################################################

# Elasticsearch

class PaginatedElasticSearchListAPIView(generics.ListAPIView):
    """List APIView to implement query search with elasticsearch engine"""

    # Note: To use this class, we have to provide our:
    #       1-  url kwargs have query string value using given key.
    #       2-  model class.
    #       3-  filter lookup that will be use in lookup expression to retrieve
    #           data from database.
    #       4-  filter keyword that will use in elastic search filter.
    #       5-  filter exclude argument that will exclude some result from
    #           filter search.
    #       6-  filter exclude value for filter exclude argument.
    #       7-  filter order by value.
    #       8-  serializer class.
    #       9-  document class.
    #       10- pagination class (optional).
    #       11- override generate_q_expression() method.

    # Define attributes.
    kwargs_query = 'query'
    model_class = None
    filter_lookup = None
    filter_keyword = None
    filter_exclude_arg = None
    filter_exclude_val = None
    filter_order_by = None
    serializer_class = None
    document_class = None
    pagination_class = pagination.PageNumberPaginationNoCount

    @abc.abstractmethod
    def generate_q_expression(self, query):
        """This method should be overridden and return a Q() expression for
        elasticsearch"""

    def get_search_response(self):
        """Method to return response from search engine for a given query
        string"""

        # Important: this class view implement pagination, so the method
        #            get_queryset() doesn't return anything when you haven't
        #            filled something in for query. Hence, it returns None
        #            which isn't a valid QuerySet or iterable. As such Django
        #            can't call len() on it for pagination process, so you have
        #            to return an empty list or queryset.

        # Note: if you want to know the elasticsearch parameters that can be
        #       used with query, go to 'Search(Request)' class in search.py
        #       file of 'elasticsearch_dsl' package and check its methods.

        # Get query string as lower case from url parameter (argument).
        kwarg_query = self.kwargs.get(self.kwargs_query, None)

        try:
            # pass query to generate_q_expression() (the overriden version).
            q = self.generate_q_expression(kwarg_query)

            # Set Q() expression query to be searched within provided document.
            search = self.document_class.search().query(q)

            # Exclude items from your query
            # search = search.exclude('<field_name>', draft=True)

            # Filter documents that contain terms within a provided range.
            # eg: the posts created for the past day (1d)
            # search = search.filter('range', <field_name>={"gte": "now-1d"})

            # Ordering
            # Note: prefixed by the - sign with specific field name to specify
            #       a descending order.
            # search = search.sort('<field_name>')

            # Selectively control how the _source field is returned.
            search = search.source(fields=[self.filter_keyword])

            # Trigger the query search of elasticsearch.
            # Note: Retrieved data will be list of document type (table)
            #       instance that set as document_class property of this class.
            elasticsearch_response = search.execute()

            # print(
            #     f"Found {elasticsearch_response.hits.total.value} "
            #     f"hit(s) for query: {kwarg_query}"
            # )

            return elasticsearch_response

        except Exception as e:
            logging.exception(e)
            return []

    def get_queryset(self):
        """Return given model class instance/instances if there are hits from
        search engine"""

        # Get value of search response.
        search_response = self.get_search_response()

        # Check that count of search hits is bigger than 0
        if hasattr(search_response, "hits") and \
                search_response.hits.total.value > 0:

            # Construct the full lookup expression.
            lookup = '__'.join([self.filter_lookup, 'in'])

            # Create list of filter_keyword string from search response.
            lookup_vals = [ele[self.filter_keyword] for ele in search_response]

            # if filter exclude argument is not None
            if self.filter_exclude_arg:
                # Get the filtered queryset for provided model class.
                queryset = self.model_class.objects.filter(
                    **{lookup: lookup_vals}
                ).exclude(
                    **{self.filter_exclude_arg: self.filter_exclude_val}
                ).distinct().order_by(self.filter_order_by)

            else:
                # Get the filtered queryset for provided model class.
                queryset = self.model_class.objects.filter(
                    **{lookup: lookup_vals}
                ).distinct().order_by(self.filter_order_by)

            # make sure queryset return no-empty list
            if queryset:
                return queryset
            else:
                return []
        else:
            return []


#########################################################################

# Multi-use

class CountryCheckAPIView(views.APIView):
    """APIView to check country"""

    def post(self, request, data=None):
        """HTTP POST method"""

        # Data attribute value for this view POST method should be:
        # {
        #   "title": <value>
        #   "iso_code": <value>
        # }

        # Set what dictionary to use.
        to_use = data if data else request.data

        # Get the 'title' and 'iso_code' property value from data of HTTP POST
        # request.
        title = to_use.get('title', None)
        iso_code = to_use.get('iso_code', None)

        # Check if country title is not empty/zero/None
        if title:
            try:
                # Get the country instance using ignore case for string of
                # provided country title.
                country_instance = Country.objects.get(
                    title__iexact=title,
                    is_available=True
                )

                # Check if country iso code is not empty/zero/None
                if iso_code:

                    # check that the retrieved instance iso code is the same
                    # as provide iso code in HTTP request, otherwise raise an
                    # exception.
                    if country_instance.iso_code != iso_code:

                        return Response(
                            {
                                'message':
                                    exceptions.
                                    InvalidCountryIsoCode.default_detail,
                                'default_code':
                                    exceptions.
                                    InvalidCountryIsoCode.default_code,
                                'iso_code': iso_code
                            },
                            status=exceptions.
                            InvalidCountryIsoCode.status_code,
                        )

                # In case everything went ok.
                return Response(
                    {
                        "title": country_instance.title,
                        "iso_code": country_instance.iso_code
                    },
                    status=status.HTTP_200_OK
                )

            except ObjectDoesNotExist:
                return Response(
                    {
                        'message':
                            exceptions.InvalidCountryTitle.default_detail,
                        'default_code':
                            exceptions.InvalidCountryTitle.default_code,
                        'title': title
                    },
                    status=exceptions.InvalidCountryTitle.status_code,
                )

        # In case no country title is provided, check if country iso code is
        # not empty/zero/None
        elif iso_code:
            try:
                # Get the country iso code instance using ignore case for
                # string of provided country title.
                country_instance = Country.objects.get(
                    iso_code__iexact=iso_code,
                    is_available=True
                )

                # In case everything went ok.
                return Response(
                    {
                        "title": country_instance.title,
                        "iso_code": country_instance.iso_code
                    },
                    status=status.HTTP_200_OK
                )

            except ObjectDoesNotExist:
                return Response(
                    {
                        'message':
                            exceptions.InvalidCountryIsoCode.default_detail,
                        'default_code':
                            exceptions.InvalidCountryIsoCode.default_code,
                        'iso_code': iso_code
                    },
                    status=exceptions.InvalidCountryIsoCode.status_code,
                )
        else:
            # In case no country or iso code has provided
            return Response(
                {
                    'message': "No country title or iso-code has provided"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class AddressCheckAPIView(views.APIView):
    """ApiView to check address"""

    def post(self, request, data=None):
        """HTTP post method"""

        # Data attribute value for this view POST method should be:
        # {
        #   "country": { # possible, one of them
        #       "title": <value>,
        #       "iso_code": <value>
        #   },
        #   "address_details": {
        #       "address1": <value>,
        #       "address2": <value>, # Not required
        #       "region": <value>,
        #       "city": <value>,
        #       "postal_code": <value> # Not required
        #   }
        # }
        #

        # Set what dictionary to use.
        to_use = data if data else request.data

        country = to_use.get('country', None)
        address_details = to_use.get('address_details', None)

        try:
            if country:

                # Initialize an empty dictionary to hold data to use with other
                # API view.
                data = {}

                # Set required properties value.
                if country.get('title', None):
                    data['title'] = country['title']

                if country.get('iso_code', None):
                    data['iso_code'] = country['iso_code']

                country_check_res = CountryCheckAPIView().post(
                    request=request,
                    data=data
                )

                if country_check_res.status_code != status.HTTP_200_OK:
                    return Response(
                        country_check_res.data,
                        status=country_check_res.status_code
                    )

                # check if address details is provided.
                if address_details:

                    # Validate address details with serializer class.
                    serializer = serializers.AddressCheckSerializer(
                        data=address_details
                    )

                    if serializer.is_valid():
                        return Response(
                            {
                                "country": country_check_res.data,
                                "address_details": serializer.data
                            },
                            status=status.HTTP_200_OK
                        )
                    else:
                        return Response(
                            serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST
                        )

                else:
                    return Response(
                        {
                            "message": "No address details have provided"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            else:
                return Response(
                    {
                        "message": "No country title or iso code has provided"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            logging.exception(e)
            return Response(
                {
                    "message": "Error is occurred while trying to check "
                               "address"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PersonalInfoCheckAPIView(views.APIView):
    """ApiView to check personal info"""

    def post(self, request, data=None):
        """HTTP POST method"""

        # Data attribute value for this view POST method should be:
        # {
        #   "first_name": <value>,
        #   "last_name": <value>,
        #   "email": <value>,
        #   "phone_number": <value>
        # }

        to_use = data if data else request.data

        first_name = to_use.get("first_name", None)
        last_name = to_use.get("last_name", None)
        email = to_use.get("email", None)
        phone_number = to_use.get("phone_number", None)

        # Validate address details with serializer class.
        serializer = serializers.ProfileCheckSerializer(
            data={
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone_number": phone_number
            }
        )

        if serializer.is_valid():
            return Response(
                {
                    'personal_info': {
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "phone_number": phone_number
                    }
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
