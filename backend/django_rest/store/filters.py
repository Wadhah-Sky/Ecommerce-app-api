""" Set the filter classes for the api"""

from django_filters import rest_framework as filters
from django_filters.constants import EMPTY_VALUES

from django.db.models import Q, Case, When

from functools import reduce
from operator import or_
from itertools import product

from core.models import Product, ProductItem
from store import exceptions


# Important: the django filters are using main queryset of the View related
#            class, so they are just do filter for that queryset like filter()
#            ORM method.


# Info: You should use hyphens in a crawlable web application URL. Why?
#       Because the hyphen separates words (so that a search engine can index
#       the individual words), and a hyphen is not a word character. Underscore
#       is a word character, meaning it should be considered part of a word.
#       'camelCase' and 'underscore' also require the user to use the shift
#       key, whereas hyphenated does not.

# Info: Without going into too much detail, filters and filtersets are just an
#       extension of Django's forms:
#       1- 'Filter' has a form Field, which in turn has a Widget.
#       2- 'FilterSet' is composed of Filters.
#       3- 'FilterSet' generates an inner form based on its filters' fields.
#
#       Responsibilities of each filter component:
#
#       1- The widget retrieves the raw value from the data QueryDict.
#       2- The field validates the raw value.
#       3- The filter constructs the filter() call to the queryset, using the
#          validated value.
#
#       In order to apply multiple values for the same filter, you would need
#       a filter, field, and widget that understand how to operate on multiple
#       values.

# Info: You can use a form class inside your FilterSet class to validate and
#       return cleaned_data object.

# Note: filtering is the data options that can be used to filter certain
#       view queryset, so don't restrict your filter class to use specific data
#       options depending on the view request parameters because this will make
#       it too complex and inflexible to be use filter with other url but that
#       have different parameters.


# How to use conditional lambda?
#
# lambda <arguments> : <Return Value if True> if <condition>
#                      else <Return Value if condition is False>

# sort() vs sorted?
#
# 1- sorted() working on both of list/tuple data type. while sort() only list.
# 2- sorted() create new sorted value, while sort() change the original value.

# How to use sorted with 2D list, like sorting depending on index 1 of row?
#
# sorted(<2D_list>, key=itemgetter(1))
#
# * itemgetter will select the row while provided value select index in the row

# Info: According to the Python documentation, an iterable is any object that
#       can return its members one at a time. By definition, iterables support
#       the iterator protocol, which specifies how object members are returned
#       when an object is used in an iterator. Python has two commonly used
#       types of iterables:
#
#       1- Sequences
#       2- Generators
#
#       Any iterable can be used in a for loop, but only sequences can be
#       accessed by integer indices. Trying to access items by index from
#       a generator or an iterator will raise a TypeError:

# How to use enumerate()?
#
# enumerate generate a generator without need to advance your index and
# remember where you are in the loop, You can use enumerate() in a loop in
# almost the same way that you use the original iterable object. Instead of
# putting the iterable directly after in the for loop, you put it inside the
# parentheses of enumerate().
# Also, you can set the starter to start your loop from in provided object:
#
# for count, value in enumerate(values, start=1):
#      print(count, value)

# What is class Case() in django models?
#
# A Case() expression is like the if … elif … else statement in Python. Each
# condition in the provided When() objects is evaluated in order, until one
# evaluates to a truthful value. The result expression from the matching When()
# object is returned:
#
# Client.objects.annotate(
#      discount=Case(
#          When(account_type=Client.GOLD, then=Value('5%')),
#          When(account_type=Client.PLATINUM, then=Value('10%')),
#          default=Value('0%'),
#      ),
# )


class StringSeperatedByCommaFilter(filters.Filter):
    """Custom filter class to create a list of values from query_parameter of
    view url where its value is a string can contain a comma as mark to
    multiple values"""

    # Instead of default behavior of filtering the query_parameter value of
    # ModelMultipleChoiceFilter class, ex:
    # /api/v1/store/.../?brand=value1&brand=value2&brand=value3...
    #
    # We can do this:
    # /api/v1/store/.../?brand=value1,value2,value3...

    def filter(self, qs, value):
        """Override the default behavior of filter() method of class Filter
        that used to filter the return value of view queryset"""

        # Note: the parameters:
        # qs: represent the queryset of view
        # value: represent the value of url_parameter of Meta.fields

        # EMPTY_VALUES = ([], (), {}, "", None)
        if value in EMPTY_VALUES:
            return qs

        # Here the important part where take the whole string of 'value' and
        # convert it to list using comma ',' as seperator.
        value_list = value.split(',')

        # Now update queryset to have the same default filter(self, qs, value)
        # method of Filter class (super) but set the 'value' parameter to be a
        # list of values, e.g.:
        # ModelName.objects.filter(field_name__lookup_expr=value_list)
        qs = super(StringSeperatedByCommaFilter, self).filter(qs, value_list)

        # Return the updated queryset to the view's 'filter_backends'.
        return qs


class ProductBackendFilter(filters.DjangoFilterBackend):
    """class which helps us to filter the view queryset with complex lookups
     and some other stuff."""

    # Info: DRF has few built-in backends which can be found here.DRF
    #        official docs recommend to use django-filter package for advanced
    #        filtering purposes.

    # Note: Using a filter backend allows you to more easily add this
    #       restriction to multiple views, or to apply it across the entire API

    def get_filterset_kwargs(self, request, queryset, view):
        """Override the backend related method with the one has defined in
           the view"""

        # Note: if you update filterset_kwargs with new data, you need to
        #       override the __init__ method of FilterSet class.
        #       Also, you can access kwargs in FilterSet class through
        #       'self.request'

        kwargs = super().get_filterset_kwargs(request, queryset, view)

        # merge filterset kwargs provided by view class
        if hasattr(view, 'get_filterset_kwargs'):
            kwargs.update(view.get_filterset_kwargs())

        # return {
        #     "data": request.query_params,
        #     "queryset": queryset,
        #     "request": request,
        # }

        # OR

        return kwargs

    # def filter_queryset(self, request, queryset, view):
    #     """Method to override the filter backend queryset, The method should
    #     return a new, filtered queryset"""
    #
    #     return queryset.filter(owner=request.user)


class ProductFilter(filters.FilterSet):
    """Class that provide filtering options for the queryset of Product model
    when retrieved by the view serializer"""

    class Meta:
        """Set metadata for the filter class"""

        # set the model that will use, it's the same one that is being use in
        # view queryset.
        model = Product
        # set the fields of that model or NOT that can be use as filter options
        # Note: these fields will use as query parameters and not necessary
        #       have to be fields defined in the specified model class, BUT you
        #       should add customized queries (the ones that use customized
        #       'Filter' class)
        #
        fields = ['attr']
        # filter_overrides = {
        #     CharField: {
        #         'filter_class': CharFilter,
        #         'extra': lambda f: {
        #             'lookup_expr': 'icontains',
        #         },
        #     },
        #     BooleanField: {
        #         'filter_class': BooleanFilter,
        #         'extra': lambda f: {
        #             'widget': CheckboxInput,
        #         },
        #     },
        # }

    def __init__(self, titles=None, selected_items_dict=None, *args,
                 **kwargs):
        """Do something with the filter or with the updated/added objects in
        backend filterset_kwargs"""

        super().__init__(*args, **kwargs)

        # Note: self.data is QueryDict data type.
        data = self.data

        # Set class attribute 'titles' with customized list of lists passed
        # argument from backend filter class.
        self.titles = titles

        # Set class attribute 'selected_items_dict' with customized
        # dictionary variable => {'product_pk': 'item_instance'}.
        self.selected_items_dict = selected_items_dict

        # You can validate the data arguments.
        min_price = data.get('min_price', None)
        max_price = data.get('max_price', None)

        # Our price validation should be, we do the same to frontend validation
        #
        # Min price => 0 - 4999
        # Max price => 0 - 5000

        # Get the USD min and max prices amount from ProductItem model.
        # Note: we do same validation on frontend.
        usd_min_amount = ProductItem.USD_MIN_PRICE_AMOUNT
        usd_max_amount = ProductItem.USD_MAX_PRICE_AMOUNT

        # Note: "-1" and "1.5" are NOT considered numeric values, because all
        #       the characters in the string must be numeric, and the - and
        #       the . are not.

        if min_price:
            # Check if min_price value is numeric or not.
            if not min_price.isnumeric():
                raise exceptions.InvalidPriceValueDataType

            # Validate the value of min_price query string, and raise an
            # api exception if it's not valid.
            elif int(min_price) < usd_min_amount or \
                    int(min_price) >= usd_max_amount:
                raise exceptions.InvalidMinPriceValue

        if max_price:
            # Check if max_price value is numeric or not.
            if not max_price.isnumeric():
                raise exceptions.InvalidPriceValueDataType

            # Validate the value of max_price query string, and raise an
            # api exception if it's not valid.
            if int(max_price) < usd_min_amount or\
                    int(max_price) > usd_max_amount:
                raise exceptions.InvalidMaxPriceValue

        if min_price and max_price:
            # Validate that max price value is bigger than min price value.
            if int(min_price) > int(max_price):
                raise exceptions.InvalidMinMaxPriceValue

    # Specify fields type of Meta.fields/extra which will be use as
    # 'query_parameter' for the view url to retrieve filtered queryset.

    # attr = filters.ModelMultipleChoiceFilter(
    #     # set field name value for Meta.model.objects.filter
    #     # here we are using foreign key object
    #     field_name='product_attributes_product__attribute__title',
    #     # the actual field name of that foreign key-model, default is 'id'.
    #     to_field_name='title',
    #     # ModelMultipleChoiceFilter using lookup expr (in) (means OR |), and
    #     # you can set to be AND (.fiter) be set conjoined to be True.
    #     conjoined=True,
    #     # queryset to get selectable objects that can be used as value to
    #     # 'field_name' depends on 'to_field_name' value.
    #     queryset=Attribute.objects.filter(leaf_nodes__isnull=True),
    #     # widget that will use to show available object options to be use in
    #     # form box in rest framework browsable api page.
    #     widget=CheckboxSelectMultiple(),
    #     # label for widget in form box.
    #     label="Attribute siblings",
    #     # suffix after label of widget.
    #     label_suffix="",
    # )

    attr = StringSeperatedByCommaFilter(
        field_name="product_attributes_product__attribute__title",
        method="filter_attr",
        label="Attributes string seperated by comma"
    )

    min_price = filters.NumberFilter(
        method="filter_min_price",
        label="Min price for product items"
    )
    max_price = filters.NumberFilter(
        method="filter_max_price",
        label="Max price for product items"
    )

    select_by = filters.OrderingFilter(
        # You can set possible available parameters to select by, use list of
        # tuples that each tuple have two values (parameter, shown value).
        choices=[
            ('deals', 'Deals'),
            ('price-high-to-low', 'Price: High to Low'),
            ('price-low-to-high', 'Price: Low to High')
        ],
        method='filter_select_by',
        label="Select by"
    )

    # Note: To filter the primary queryset by the request object, simply
    #       override the 'FilterSet.qs' property.

    # @property
    # def qs(self):
    #     """Override 'FilterSet.qs' property"""
    #
    #     # get FilterSet.qs
    #     parent = super().qs
    #
    #     # Get author value from request.
    #     author = getattr(self.request, 'user', None)
    #
    #     # Filter the primary/main queryset.
    #     return parent.filter(is_published=True) |parent.filter(author=author)

    def filter_attr(self, queryset, name, value):
        """customized method for attr argument of filter set"""

        # queryset: represent the backend queryset
        # name: represent the field_name if had been set.
        # value: represent the argument value in URL.

        # Construct the full lookup expression.
        lookup = '__'.join([name, 'in'])

        # Initialize the list of lists from class instance attribute 'titles'.
        titles = self.titles

        # In case titles list is empty, return the None which means there
        # is no matching.
        if not titles:
            return queryset.none()

        # No need to go through long process if there is only one item in set.
        elif len(titles) > 1:

            #############################################################

            # This part of code for learn purpose:

            # Get max length of list item inside list.
            # Info: map(function, iterator) will execute function on iterator
            #       items.
            # length = max(map(len, titles))

            # Get items count of list.
            # items_count = len(looped_instances)

            # Loop over range of items_count to create 2D array(list of lists)
            # for i in range(items_count):
            #     # Add an empty list defined list. Rows
            #     list_of_lists.append([])
            #
            #     # Loop over range length.
            #     for j in range(length):
            #         # Add for each item [i] value of None. Columns
            #         list_of_lists[i].append(None)

            #############################################################

            # Cartesian product: (this method for create dictionary of tuples
            # that each tuple contain a unique values from a list of lists that
            # provided).
            # Note: Cartesian product returns duplicate tuples.

            # Get Set of dictionary of tuples and convert it to list as
            # Cartesian product.
            cartesian_product = list(set(product(*titles)))

            # Initialize empty list for queries, since we need to do
            # queries on sub-tuple items of cartesian_product as AND
            # (.filter) and between the sub-tuples as OR (Q(|)).
            queries = []

            # Loop over cartesian_product tuples.
            for t_item in cartesian_product:
                # We set new query as the provided queryset list.
                query = queryset
                # Loop over t_item
                for attribute in t_item:
                    # For each item in tuple in cartesian_product do
                    # (.filter) on.
                    # We use Q() object that can take a 2-tuple where first
                    # item is string that specifies the "key" while second item
                    # the "value".
                    # Here key is the defined 'field_name' while value is
                    # 'attribute':
                    #
                    # queryset.filter(<field_name>=attribute)
                    #
                    query = query.filter(Q((name, attribute)))

                # Append list of query into queries list.
                queries.append(query)

            # Info: The reduce(fun,seq) function is used to apply
            #       a particular function passed in its argument to all the
            #       list elements mentioned in the sequence passed along,
            #       can be combined with lambda or operator interface
            #       functions e.g. add, mul, or_ ..etc

            # Now for each query list in 'queries' we connect them with OR
            # operator.
            queryset = reduce(or_, queries)

            return queryset

        # In case only one value passed within query parameter.
        else:
            # This is in case you want to set lookup with value.
            # Note: since our lookup expr using (in), so our value should be
            #       iterable (list, set or tuple).
            return queryset.filter(**{lookup: titles[0]})

            # alternatively, you could opt to hardcode the lookup after remove
            # 'field_name' from your argument filter. e.g.,
            # return queryset.filter(published_on__isnull=False)

    def filter_min_price(self, queryset, name, value):
        """customized method for min_price argument of filter set"""

        # queryset: represent the backend queryset
        # name: represent the field_name if had been set.
        # value: represent the argument value in URL.

        # Initialize an empty list to store 'pk' of conditional products.
        products = []

        # Loop over queryset of products.
        for prod in queryset:

            # Loop over current product instance items.
            # if you search depending on items, use 'break' when condition is
            # true
            # for item in product.product_items_product.all():

            # Initialize instance variable.
            instance_var = None

            # Return the product item instance if this product 'pk' if found in
            # the dictionary, or return None.
            if self.selected_items_dict:
                instance_var = self.selected_items_dict[prod.pk]

            # Check if current product return a item_deal_price property value.
            if prod.item_deal_price(item=instance_var):

                # Check if item_deal_price is bigger than equal provided value.
                if prod.item_deal_price(item=instance_var).amount >= value:

                    # If so, append current product 'pk' into products list
                    # and break the loop.
                    products.append(prod.pk)

            # In case the current item don't have item_deal_price, check its
            # item_list_price is bigger than equal provided value or not.
            elif prod.item_list_price(item=instance_var).amount >= value:
                products.append(prod.pk)

        # return the queryset for certain products.
        return queryset.filter(pk__in=products)

    def filter_max_price(self, queryset, name, value):
        """customized method for max_price argument of filter set"""

        # queryset: represent the backend queryset
        # name: represent the field_name if had been set.
        # value: represent the argument value in URL.

        # Initialize an empty list to store 'pk' of conditional products.
        products = []

        # Loop over queryset of products.
        for prod in queryset:

            # Initialize instance variable.
            instance_var = None

            # Return the product item instance if this product 'pk' if found in
            # the dictionary, or return None.
            if self.selected_items_dict:
                instance_var = self.selected_items_dict[prod.pk]

            # Check if current product return a item_deal_price property value.
            if prod.item_deal_price(item=instance_var):

                # Check if item_deal_price is less than equal provided
                # value.
                if prod.item_deal_price(item=instance_var).amount <= value:
                    # If so, append current product 'pk' into products list
                    # and break the loop.
                    products.append(prod.pk)

            # In case the current product don't have item_deal_price, check its
            # item_instance is less than equal provided value or not.
            elif prod.item_list_price(item=instance_var).amount <= value:
                products.append(prod.pk)

        # return the queryset for certain products.
        return queryset.filter(pk__in=products)

    def sorting_price(self, queryset, reverse=False):
        """Method to sort queryset of Product model depending on price"""

        # Info: if reverse is False, means sorting will be from low to high.

        def get_list_price(prod):
            """Return the list price as Money for product OR product_item
            instance if exists in dictionary"""

            # Initialize instance variable.
            instance_var = self.selected_items_dict[prod.pk] or None

            # Get list price as Money.
            money = prod.item_list_price(item=instance_var)

            return money

        def get_is_has_deal_price(prod):
            """Return True if product instance 'pk' is found in the dictionary
            And the selected product item instance has deal price"""

            # Initialize instance variable.
            product_item = self.selected_items_dict[prod.pk] or None

            if product_item and product_item.deal_price:
                return True
            else:
                return False

        def get_deal_price(prod):
            """Return the deal price as Money for product OR product_item
            instance if exists in dictionary"""

            # Initialize instance variable.
            instance_var = self.selected_items_dict[prod.pk] or None

            # Get deal price as Money.
            money = prod.item_deal_price(item=instance_var)

            return money

        # Info: sorted()/sort() methods working fine with value of Money.

        # if dictionary has selected item/items for current queryset products.
        if self.selected_items_dict:

            # Return a sorted list of model instances, in case they/their
            # product item have deal price or list price.

            # Important: Be careful here, you should return list/deal price for
            #            product item of each query instance in case that
            #            instance 'pk' is found in the dictionary.
            sorted_products = sorted(
                queryset,
                key=lambda instance:
                get_deal_price(prod=instance)
                if get_is_has_deal_price(prod=instance)
                else get_list_price(prod=instance),
                reverse=reverse
            )

        else:
            # Return a sorted list of model instances, in case they have deal
            # price or item list price.

            # This is in case you trying to sort against value of instance
            # property, use:
            #
            # getattr(instance, '<property>')
            #
            # sorted_products = sorted(
            #                 queryset,
            #                 key=lambda instance:
            #                 getattr(instance, 'item_deal_price')
            #                 if instance.item_deal_price
            #                 else getattr(instance, 'item_list_price'),
            #                 reverse=reverse
            #             )
            #

            sorted_products = sorted(
                queryset,
                key=lambda instance:
                instance.item_deal_price()
                if instance.item_deal_price()
                else instance.item_list_price(),
                reverse=reverse
            )

        # Get the list 'pk' of sorted products.
        pk_list = [instance.pk for instance in sorted_products]

        # Write a Case of list arguments (*) of pk for queryset, when value of
        # current enumerate iterate is equal to 'pk' then set the position of
        # current iterate as value to the 'preserved' list.
        # Info: this will re-order the queryset list depending on position
        #       value of enumerate.
        preserved = Case(
            *[When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)]
        )

        # ORM order_by() is kind of sorted method.
        return queryset.filter(pk__in=pk_list).order_by(preserved)

    def filter_select_by(self, queryset, name, value):
        """customized method for select_by"""

        # queryset: represent the backend queryset
        # name: represent the field_name if had been set.
        # value: represent the argument value in URL.

        # Note: if the user provide parameter name that not exists within
        #       'filters.OrderingFilter' choices, will raise api exception.
        #       Also you should return a queryset for all possible choices
        #       otherwise will raise 'NoneType' exception.

        # By default, the value of 'filters.OrderingFilter' class is an array
        # of possible choices parameters.
        for choice in value:

            # Check if parameter string is 'deals'.
            if str(choice).lower() == 'deals':

                # Initialize an empty list to store 'pk' of conditional
                # products.
                products = []

                # Loop over queryset of products.
                for prod in queryset:

                    # Initialize instance variable.
                    instance_var = None

                    # Return the product item instance if this product 'pk' if
                    # found in the dictionary, or return None.
                    if self.selected_items_dict:
                        instance_var = self.selected_items_dict[prod.pk]

                    # Check if current item return a deal_price property value.
                    if prod.item_deal_price(instance_var):
                        # If so, append current product 'pk' into products
                        # list
                        products.append(prod.pk)

                # return the queryset for certain products.
                return queryset.filter(pk__in=products)

            # Check if parameter string is 'low-to-high'.
            if str(choice).lower() == 'price-low-to-high':

                return self.sorting_price(queryset, reverse=False)

            # Check if parameter string is 'high-to-low'.
            if str(choice).lower() == 'price-high-to-low':

                return self.sorting_price(queryset, reverse=True)

            else:
                return queryset.none()
