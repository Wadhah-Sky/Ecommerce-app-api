"""Register your backend views"""

from django.urls import path
# from django import forms

# from dal import autocomplete

from core import views

# import djhacker

# Define a variable that help to identify which api that creating URL from when
# using reverse function.
app_name = 'core'

urlpatterns = [
    path(
        'attribute-autocomplete/',
        views.AttributeAutocompleteView.as_view(),
        name='attribute-autocomplete',
    ),
    path(
        'country/check/',
        views.CountryCheckAPIView.as_view(),
        name='country_check'
    ),
    path(
        'address/check/',
        views.AddressCheckAPIView.as_view(),
        name='address_check'
    ),
    path(
        'personal-info/check/',
        views.PersonalInfoCheckAPIView.as_view(),
        name='personal_info_check'
    )

    # path(
    #     'size-autocomplete/',
    #     views.SizeAutocompleteView.as_view(),
    #     name='size-autocomplete',
    # ),
]

# Now hack your model field to always render the autocomplete field with
# that view!
# djhacker.formfield(
#     # Specify the field of the model.
#     models.ProductOption.attribute_option,
#     # Specify the form field type, since our field is a Foreign key, so we
#     # set it to be choice field.
#     forms.ModelChoiceField,
#     # Set the widget for this form field.
#     widget=autocomplete.ModelSelect2(
#         # Set your django api url:
#         # '<api name>:<name of the registered view path>'
#         #
#         # Note: make sure you registered the api routes in your main
#         # 'urls.py' file.
#         url='core:attribute-option-autocomplete',
#         # Forward the selected/parent/sub form fields to the
#         # autocomplete view.
#         # Note: if you forward relational model field, the value that
#         #       will pass is actual obj of that field as pk.
#         # You have four ways to pass fields and can be mixed, better
#         # to use tuple to do it:
#         # 1- using related form field name:
#         #
#         #    forward=('category',)
#         #
#         # 2- using dal.forward.Field class to pass field name as
#         #    specific name:
#         #
#         #   forward=(dal.forward.Field(
#         #            <field_name>, <renamed_field_name>
#         #        ),
#         #   )
#         #
#         # 3- using dal.forward.Const class to pass arbitrary constant
#         #    which means the name is not related to any field in the form:
#         #
#         #    forward=(dal.forward.Const(True, <arbitrary_constant_name>),)
#         #
#         # 4- using dal.forward.JavaScript class to pass customize html
#         #    field, For these cases DAL provides a way to customize
#         #    forwarding logic using JS callbacks. You can register JS
#         #    forward handler on your page:
#         #
#         #    forward=(dal.forward.JavaScript(
#         #          'my_awesome_handler', 'magic_number'
#         #        ),
#         #    )
#         #
#         # Info: You can forward own selected value by using:
#         #
#         #       forward=(dal.forward.Self(),)
#         #
#         forward=(
#              'category',
#              forward.Const(True, 'is_item_option')
#         ),
#         # You can set some options for this Select2 field.
#         attrs={
#             # Set placeholder
#             'data-placeholder': 'category related attribute options'
#         },
#     )
# )
