from django import forms

# from durationwidget.widgets import TimeDurationWidget

from dal import autocomplete
from dal import forward

from core.models import ProductItemAttribute, ProductAttribute


class ProductItemAttributeInlineForm(forms.ModelForm):
    """Form class for admin add/change page of ProductItemAttribute model"""

    class Meta:
        model = ProductItemAttribute
        exclude = ['id']
        # fields = '__all__'

        # Set your fields widget.
        widgets = {
            # For 'attribute_option' field, we need to be depended on
            # 'category' field value in 'Product' model.
            # We will use 'dal' and 'dal_select2' packages to achieve that.
            'product_attribute': autocomplete.ModelSelect2(
                # Set your django api url:
                # '<api name>:<name of the registered view path>'
                #
                # Note: make sure you registered the api routes in your main
                # project 'urls.py' file.
                url='core:attribute-autocomplete',
                # Forward the selected/parent/sub form fields to the
                # autocomplete view.
                # Note: if you forward relational model field, the value that
                #       will pass is actual obj of that field as pk.
                # You have four ways to pass fields and can be mixed, better
                # to use tuple to do it:
                # 1- using related form field name:
                #
                #    forward=('category',)
                #
                # 2- using dal.forward.Field class to pass field name as
                #    specific name:
                #
                #   forward=(dal.forward.Field(
                #            <field_name>, <renamed_field_name>
                #        ),
                #   )
                #
                # 3- using dal.forward.Const class to pass arbitrary constant
                #    which means the name is not related to any field in the
                #    form:
                #
                #    forward=(dal.forward.Const(
                #                  True,
                #                  <arbitrary_constant_name>),
                #    )
                #
                # 4- using dal.forward.JavaScript class to pass customize html
                #    field, For these cases DAL provides a way to customize
                #    forwarding logic using JS callbacks. You can register JS
                #    forward handler on your page:
                #
                #    forward=(dal.forward.JavaScript(
                #          'my_awesome_handler', 'magic_number'
                #        ),
                #    )
                #
                # Info: You can forward own selected value by using:
                #
                #       forward=(dal.forward.Self(),)
                #
                forward=(
                    'category',
                    'product',
                    forward.Const(False, 'is_common_attribute')
                ),
                # You can set some options for this Select2 field.
                attrs={
                    # Set placeholder
                    'data-placeholder': 'product related attributes'
                },
            ),
        }


class ProductAttributeInlineForm(forms.ModelForm):
    """Form class for admin add/change page of ProductAttribute model"""

    class Meta:
        model = ProductAttribute
        exclude = ['id']
        # fields = '__all__'

        # Set your fields widget.
        widgets = {
            'attribute': autocomplete.ModelSelect2(
                url='core:attribute-autocomplete',
                forward=('category',),
                attrs={
                    # Set placeholder
                    'data-placeholder': 'category related attributes'
                },
            ),
        }


# class ProductAdminForm(forms.ModelForm):
#     """Form class for admin add/change page of ProductOption model"""
#
#     class Meta:
#         model = Product
#         exclude = ['id']
#         # fields = '__all__'
#
#         # Set your fields widget.
#         widgets = {
#             'brand_category': autocomplete.ModelSelect2(
#                 # Set your django api url:
#                 # '<api name>:<name of the registered view path>'
#                 #
#                 # Note: make sure you registered the api routes in your main
#                 # project 'urls.py' file.
#                 url='core:brand-category-autocomplete',
#                 # Set the related model field value to pass it to the view.
#                 # Note: if you forward relational model field, the value that
#                 #       will pass is actual obj of that field.
#                 forward={'category': Product.category},
#                 # You can set some options for this Select2 field.
#                 attrs={
#                     # Set placeholder
#                     'data-placeholder': 'category related brands'
#                 },
#             ),
#         }
