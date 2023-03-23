"""Register the views for this backend"""

from django.views.generic.base import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.http import (HttpResponseNotFound, HttpResponseForbidden,
                         HttpResponseServerError)
from django.db.models import Subquery

from dal import autocomplete

from core.models import Category, Attribute, ProductAttribute

import logging


class IndexTemplateView(TemplateView):
    """View class to render index.html template"""

    # Specify the page to be rendered with TemplateView class.
    template_name = 'index.html'


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
