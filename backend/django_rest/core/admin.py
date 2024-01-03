"""Customize and manage your project django admin web page"""

from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin import ModelAdmin as BaseModelAdmin
# from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
# from django.forms import NumberInput
# from django.db.models import SmallIntegerField
# from django.db.models import DurationField

from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

# from durationwidget.widgets import TimeDurationWidget

from imagekit.admin import AdminThumbnail
from imagekit import ImageSpec
from imagekit.processors import ResizeToFit
from imagekit.cachefiles import ImageCacheFile
from mptt.admin import MPTTModelAdmin

from core import models
from core import forms

import nested_admin


# Note: if you want to show the @property methods of your class models, then
#       you need to declare these properties in the related Admin class.
#       Info: you can't set @property method in fieldsets/add_fieldsets lists.

# Info: Django admin NOT necessary store the nested children models before
#       parent model.

# Important: If you add the name of a callable (function) to one of admin class
#            variables, the callable must be listed in readonly_fields.

# Important: When using 'nested_admin' inline classes, stay away from using the
#            field 'sortable_field_name', because it will cause an error in
#            django admin page that don't indicate which field of your form is
#            raising that error.

# Note: the required field of model that registered in django admin will be
#       shown in admin pages with <strong> black font.

# Note: if you created a custom admin class based on 'UserAdmin' for admin web
#       page, make sure to add both of variable list 'list_filter' and
#       'filter_horizontal' in case your 'User' model that connected to this
#       custom class, which don't have either of 'is_staff', 'is_superuser' or
#       'is_active', and these filters will be used for admin 'list' webpage.

# Note: Django uses metaclass to create the actual class based on the class
#       definition your provide. In brief, upon instantiation of your model
#       class, the metaclass will run through your model field definitions and
#       return a corresponding class with the appropriate attributes.


# Note: Ordering using ModelAdmin.ordering may cause performance problems as
#       sorting on a large queryset will be slow. Also, if your 'search_fields'
#       include fields that aren’t indexed by the database, you might encounter
#       poor performance on extremely large tables.
#       For those cases:
#       1- it’s a good idea to write your own ModelAdmin.get_search_results()
#       implementation using a full-text indexed search.
#       2- You may also want to change the Paginator on very large tables as
#       the default paginator always performs a count() query. For example,
#       you could override the default implementation of the 'Paginator.count'
#       property.


def cached_admin_thumb(instance):
    """Imagekit class, to generate cached images for related model field"""

    # `thumbnail` is the name of the image field on the model
    cached = ImageCacheFile(AdminThumbnailSpec(instance.thumbnail))

    # only generates the first time, subsequent calls use cache.
    cached.generate()
    return cached


class AdminThumbnailSpec(ImageSpec):
    """Imagekit specification class"""

    # set width and height for images.
    width = 100
    height = 100

    # Define a list of  Pillow package image processors.
    processors = [ResizeToFit(width, height)]

    # Set format of image with optional options.
    format = 'JPEG'
    options = {'quality': 100}


class SiteAdmin(admin.ModelAdmin):
    """Class of Django Site model class"""

    # Note: before set this class you should do:
    #
    #       1- Add 'django.contrib.sites' to your INSTALLED_APPS setting.
    #       2- Define a SITE_ID setting, usually it's '1' unless your project
    #          serve multiple domains/subdomains:
    #
    #          SITE_ID = 1
    #       3- run 'migrate' command

    fields = ['id', 'name', 'domain']
    list_display = ['id', 'name', 'domain']
    list_display_links = ['name']
    search_fields = ['name', 'domain']
    readonly_fields = ['id']


class UserAddressInline(nested_admin.NestedTabularInline):
    """Class to show tabular of model info inside another model in admin
     page"""

    # Specify the model.
    model = models.UserAddress

    # Specify the form to be used.
    # form = forms.UserAddressAdminForm

    # Control the number of extra fields of the inline form will display on the
    # parent form for admin add page.
    # Note: InlineModelAdmin.get_extra() also allows you to customize the
    # number of extra forms.
    extra = 0
    # Required values that should be set.
    min_num = 0


class UserAdmin(BaseUserAdmin, nested_admin.NestedModelAdmin):
    """Customize variables of your django admin web page for User model"""

    # Set nested inline classes to look like below:
    # User<--Foreign<--UserAddress
    inlines = [UserAddressInline]

    # Override admin web page form-fields specifications.
    formfield_overrides = {
        PhoneNumberField: {
            'widget': PhoneNumberPrefixWidget(initial='IQ'),
            'help_text': _('Choose the country code.')
        },
    }

    #  Imagekit contain a class 'AdminThumbnail' for displaying specs
    #  (or even regular ImageFields) in the Django admin change list.
    #  Note: AdminThumbnail is used as a property on Django admin classes.
    admin_thumbnail = AdminThumbnail(image_field=cached_admin_thumb)

    # Specify the name of column in admin display page for the related model
    # field.
    admin_thumbnail.short_description = 'Thumbnail'

    # Customize the list display order of users in descending.
    ordering = ['-created_at']

    # Customize the list display of users.
    # Note: if customize it, you should put all unique fields of the model.
    list_display = [
        'email',
        'first_name',
        'last_name',
        'username',
        'last_login',
        'role',
        'created_at',
        'is_active'
    ]

    # Customize the links of list display fields.
    list_display_links = ['email', 'first_name', 'last_name', 'username']

    # Specify the sections and fields those will include in 'change' web page
    # for user.
    # Note: to display multiple fields on the same line, wrap those fields in
    # their own tuple, fieldsets=( (None,{'fields': (('email', 'password'))}),)
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'email', 'password'
                )
            }
        ),
        (
            _('Personal Info'),
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'username',
                    'phone_number',
                    'role',
                    'slug',
                    'thumbnail',
                    'admin_thumbnail'
                )
            }
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active', 'is_staff', 'is_superuser'
                )
            }
        ),
        (
            _('Important Dates'),
            {
                'fields': (
                    'last_login', 'created_at', 'updated_at'
                )
            }
        )
    )

    # Specify the sections and fields those will include in django admin 'add'
    # web page (DON'T include permission fields) in order create a new user,
    # and customize field size in form to be wide.
    add_fieldsets = (
        (
            None,
            {
                'classes': (
                    'wide',
                ),
                'fields': (
                    'first_name',
                    'last_name',
                    'username',
                    'email',
                    'password1',
                    'password2',
                    'phone_number',
                    'role',
                    'thumbnail'
                )
            }
        ),
    )

    # Specify read only fields in django web pages for 'User' model.
    # Note: you need to add 'admin_thumbnail' to this list in order to see
    # images of 'imagekit' model field.
    readonly_fields = [
        'admin_thumbnail',
        'slug',
        'is_superuser',
        'last_login',
        'created_at',
        'updated_at'
    ]


class MetaItemAdmin(BaseModelAdmin):
    """Customize variables of your django admin web page for MetaItem model"""

    # Imagekit contain a class 'AdminThumbnail' for displaying specs
    # (or even regular ImageFields) in the Django admin change list.
    # Note: AdminThumbnail is used as a property on Django admin classes.
    admin_thumbnail = AdminThumbnail(image_field=cached_admin_thumb)

    # Specify the name of column in admin display page for the related model
    # field.
    admin_thumbnail.short_description = 'Thumbnail'

    readonly_fields = ['admin_thumbnail', 'slug']


class MetaItemInline(admin.TabularInline):
    """Class to show tabular of model info inside another model in admin page
    """

    # Set either:
    # 1- a model to be use and has ForeignKey to the model that this inline
    #    class going to use inside.
    # 2- or you can use 'Model.m2m_field.through' concept with same conditions
    #    to show ManyToMany field as inline.
    model = models.MetaItem
    # extra default value is 3
    extra = 0
    # Controls the maximum number of forms to show in the inline
    # max_num = 4
    readonly_fields = ['slug']


class MetaAdmin(BaseModelAdmin):
    """Customize variables of your django admin web page for Meta model"""

    inlines = [MetaItemInline]


class CountryAdmin(BaseModelAdmin):
    """Customize variables of your django admin web page for Country model"""

    list_display = ['title', 'iso_code', 'is_available']
    search_fields = ['title', 'iso_code']


class PromotionAdmin(BaseModelAdmin):
    """Customize variables of your django admin web page for Promotion model"""

    # Override admin web page form-fields specifications.
    # Note: using formfield_overrides for DurationField, will not show the
    #       widget in right order, so use form class.
    # formfield_overrides = {
    #     DurationField: {
    #         'widget': TimeDurationWidget(show_seconds=False)
    #     },
    # }
    # form = forms.PromotionAdminForm

    ordering = ['created_at']
    list_display = [
        'title',
        'promotion_type',
        'discount_percentage',
        'max_use_times',
        'purchase_orders_count',
        'unlimited_use',
        'start_date',
        'end_date',
        'duration',
        'promotion_status',
        'created_at',
        'updated_at',
        'is_available'
    ]
    list_display_links = ['title']
    readonly_fields = ['created_at', 'updated_at']


class CategoryAdmin(MPTTModelAdmin):
    """Customize variables of your django admin web page for Category model"""

    # specify pixel amount for this ModelAdmin that inheritance from
    # MPTTModelAdmin:
    mptt_level_indent = 0

    # Define dictionary mapping field names to the fields (Non-Relational) that
    # it should pre-populate from, and will be used for 'add' and 'change'
    # pages.
    # Note: We comment this line of code because we are using signals to
    # create slug.
    # prepopulated_fields = {'slug': ('category_name',)}

    # Imagekit contain a class 'AdminThumbnail' for displaying specs
    # (or even regular ImageFields) in the Django admin change list.
    # Note: AdminThumbnail is used as a property on Django admin classes.
    admin_thumbnail = AdminThumbnail(image_field=cached_admin_thumb)

    # Specify the name of column in admin display page for the related model
    # field.
    admin_thumbnail.short_description = 'Thumbnail'

    # Customize the list display of product categories.
    list_display = [
        '__str__',
        'title',
        'slug',
        'display_order',
        'is_active',
        'created_at'
    ]

    # Specify the model fields those can be modified from list display page.
    list_editable = ['display_order', 'is_active']

    # Specify read only fields in django web pages for 'Category' model.
    # Note: you need to add 'admin_thumbnail' to this list in order to see
    # images of 'imagekit' model field.
    readonly_fields = ['admin_thumbnail', 'slug', 'created_at', 'updated_at']

    # Set 'search_fields' to enable a search box on the admin change list page.
    # This should be set to a list of field names that will be searched
    # whenever somebody submits a search query in that text box.
    # Note: 'search_fields' needed by 'autocomplete_fields' to change
    # select-box interface (<select>) of relational model fields to 'Select2'
    # autocomplete inputs.
    search_fields = ['__str__']


class BannerAdmin(BaseModelAdmin):
    """Customize variables of your django admin web page for Banner model"""

    admin_thumbnail = AdminThumbnail(image_field=cached_admin_thumb)
    admin_thumbnail.short_description = 'Thumbnail'

    # Customize the list display order of cards in descending.
    ordering = ['-created_at']
    list_display = [
        'title',
        'frontend_path',
        'display_order',
        'created_at',
        'updated_at',
        'is_active'
    ]
    list_display_links = ['title']
    list_editable = ['display_order']
    readonly_fields = [
        'admin_thumbnail',
        'slug',
        'created_at',
        'updated_at'
    ]

    # Specify autocomplete_fields which is a list of ForeignKey and/or
    # ManyToManyField fields you would like to change to 'Select2' autocomplete
    # inputs.
    # Important: you need to set 'search_fields' in the model class that
    #            related to relation field in django admin.
    autocomplete_fields = []


class TopBannerAdmin(BaseModelAdmin):
    """Customize variables of your django admin web page for TopBanner model"""

    # Customize the list display order of cards in descending.
    ordering = ['-created_at']
    list_display = [
        'title',
        'display_order',
        'created_at',
        'updated_at',
        'is_active'
    ]
    list_display_links = ['title']
    list_editable = ['display_order']
    readonly_fields = ['created_at', 'updated_at']


class CardAdmin(BaseModelAdmin):
    """Customize variables of your django admin web page for Card model"""

    admin_thumbnail = AdminThumbnail(image_field=cached_admin_thumb)
    admin_thumbnail.short_description = 'Thumbnail'
    ordering = ['-created_at']
    list_display = [
        'title',
        'category',
        'admin_thumbnail',
        'created_at',
        'updated_at',
    ]
    list_display_links = ['title']
    readonly_fields = [
        'admin_thumbnail',
        'slug',
        'created_at',
        'updated_at'
    ]
    search_fields = ['__str__']

    # Specify autocomplete_fields which is a list of ForeignKey and/or
    # ManyToManyField fields you would like to change to 'Select2' autocomplete
    # inputs.
    # Important: you need to set 'search_fields' in the model class that
    #            related to relation field in django admin.
    autocomplete_fields = []

    # def has_module_permission(self, request):
    #     """This django method is responsible for displaying a model in admin
    #     index if return True"""
    #
    #     return False


class SectionCardInline(admin.TabularInline):
    """Class to show tabular of model info inside another model in admin page
    """

    # Set either:
    # 1- a model to be use and has ForeignKey to the model that this inline
    #    class going to use inside.
    # 2- or you can use 'Model.m2m_field.through' concept with same conditions
    #    to show ManyToMany field as inline.
    model = models.SectionCard
    extra = 1
    # Controls the maximum number of forms to show in the inline
    max_num = 4


class SectionAdmin(BaseModelAdmin):
    """Customize variables of your django admin web page for Section model"""

    # form = forms.SectionAdminForm

    # def get_form(self, request, obj=None, **kwargs):
    #     """Admin model method to return change form depends on if trying to
    #      create new obj or change certain one"""
    #
    #     # Call the change form since the obj is already exists.
    #     if obj:
    #         return forms.HomeSectionChangeForm
    #
    #     # Call the default one that define above.
    #     return super(
    #         HomeSectionAdmin,
    #         self).get_form(request, obj, **kwargs)

    inlines = [SectionCardInline]
    ordering = ['-created_at']
    list_display = [
        'title',
        'display_order',
        'created_at',
        'updated_at',
        'is_active'
    ]
    list_display_links = ['title']

    # Specify the sections and fields those will include in 'change' web page
    # for user.
    fieldsets = (
        (
            'Details',
            {
                'fields': (
                    'title', 'display_order'
                )
            }
        ),
        (
            _('Activate This Section'),
            {
                'fields': (
                    'is_active',
                )
            }
        ),
        (
            _('Important Dates'),
            {
                'fields': (
                    'created_at', 'updated_at'
                )
            }
        )
    )

    # Specify list of ManyToMany fields that want to be filtered in change/add
    # admin page.
    # filter_horizontal = ['home_page_cards']

    readonly_fields = ['created_at', 'updated_at']


class SupplierAddressInline(admin.TabularInline):
    """Class to show tabular of model info inside another model in admin page
    """

    model = models.SupplierAddress
    extra = 0
    min_num = 0


class SupplierAdmin(BaseModelAdmin):
    """Customize variables of your django admin web page for Supplier model"""

    inlines = [SupplierAddressInline]

    # Override admin web page form-fields specifications.
    formfield_overrides = {
        PhoneNumberField: {
            'widget': PhoneNumberPrefixWidget(initial='IQ'),
            'help_text': _('Choose the country code.')
        },
    }
    ordering = ['-created_at']
    list_display = [
        'title',
        'email',
        'uuid',
        'is_available',
        'created_at',
        'updated_at',
    ]
    list_display_links = ['title', 'email']
    fieldsets = (
        (
            None,
            {
                'fields': ('title', 'email', 'uuid')
            }
        ),
        (
            _('Details'),
            {
                'fields': ('contact_name', 'phone_number')
            }
        ),
        (
            _('Permissions'),
            {
                'fields': ('is_available',)
            }
        ),
        (
            _('Important Dates'),
            {
                'fields': ('created_at', 'updated_at')
            }
        )
    )
    readonly_fields = [
        'uuid',
        'created_at',
        'updated_at'
    ]
    search_fields = ['__str__']


class POItemAdmin(BaseModelAdmin):
    """Customize variables of your django admin web page for POItem model"""

    readonly_fields = ['total_amount']

    def get_form(self, request, obj=None, **kwargs):
        """Override the form for this admin class"""

        form = super().get_form(request, obj, **kwargs)
        # Set the field 'price_per_unit' to be not required because we
        # automatically set its value within save() in model class.
        form.base_fields["price_per_unit"].required = False
        return form


class POItemInline(admin.TabularInline):
    """Class to show tabular of model info inside another model in admin page
    """

    model = models.POItem
    extra = 0
    min_num = 1
    # Controls the maximum number of forms to show in the inline
    max_num = 30
    readonly_fields = ['total_amount']
    autocomplete_fields = ['product_item']

    def get_formset(self, request, obj=None, **kwargs):
        """Override the formset for this inline admin class"""

        formset = super().get_formset(request, obj, **kwargs)
        # Set the field 'price_per_unit' to be not required because we
        # automatically set its value within save() in model class.
        formset.form.base_fields["price_per_unit"].required = False
        return formset


class ShippingMethodAdmin(BaseModelAdmin):
    """Customize variables of your django admin web page for ShippingMethod
     model"""

    # Override admin web page form-fields specifications.
    formfield_overrides = {
        PhoneNumberField: {
            'widget': PhoneNumberPrefixWidget(initial='IQ'),
            'help_text': _('Choose the country code.')
        },
    }


class POShippingAdmin(BaseModelAdmin):
    """Customize variables of your django admin web page for POShipping
     model"""

    readonly_fields = ['created_at', 'updated_at']


class POPaymentAdmin(BaseModelAdmin):
    """Customize variables of your django admin web page for POPayment model"""

    readonly_fields = ['created_at', 'updated_at']


class TaxAdmin(BaseModelAdmin):
    """Customize variables of your django admin web page for Tax model"""

    readonly_fields = ['created_at', 'updated_at']


class POProfileAdmin(BaseModelAdmin):
    """Customize variables of your django admin web page for POProfile
     model"""

    # Override admin web page form-fields specifications.
    formfield_overrides = {
        PhoneNumberField: {
            'widget': PhoneNumberPrefixWidget(initial='IQ'),
            'help_text': _('Choose the country code.')
        },
    }

    readonly_fields = ['created_at', 'updated_at']


class PurchaseOrderAdmin(BaseModelAdmin):
    """Customize variables of your django admin web page for PurchaseOrder
    model"""

    inlines = [POItemInline]
    ordering = ['created_at']
    list_display = [
        'po_code',
        'subtotal',
        'savings',
        'po_tax_percentage',
        'po_tax',
        'shipping_cost',
        'grand_total',
        'status',
        'created_at'
    ]
    list_display_links = ['po_code']

    # Note: you can't set @property method in fieldsets/add_fieldsets lists.

    # Specify the sections and fields those will include in django admin 'add'
    # web page.
    add_fieldsets = (
        (
            None,
            {
                'classes': (
                    'wide',
                ),
                'fields': (
                    'summary',
                )
            }
        ),
    )

    # Info: We can add any model's property to be shown in Add/Change page.
    readonly_fields = [
        'subtotal',
        'savings',
        'grand_total',
        'po_code',
        'created_at',
        'updated_at'
    ]
    # autocomplete_fields = []


class ProductGroupAdmin(BaseModelAdmin):
    """Customize variables of your django admin web page for ProductGroup
     model"""

    ordering = ['created_at']
    list_display = [
        'title',
        'display_order',
        'is_active',
        'created_at',
        'updated_at'
    ]
    list_display_links = ['title']
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['title']


class CategoryAttributeInline(admin.TabularInline):
    """Class to show tabular of model info inside another model in admin page
    """

    model = models.CategoryAttribute
    extra = 0
    min_num = 0


class AttributeAdmin(MPTTModelAdmin):
    """Customize variables of your django admin web page for Attribute model"""

    inlines = [CategoryAttributeInline]

    # specify pixel amount for this ModelAdmin that inheritance from
    # MPTTModelAdmin:
    mptt_level_indent = 0

    admin_thumbnail = AdminThumbnail(image_field=cached_admin_thumb)

    # Specify the name of column in admin display page for the related model
    # field.
    admin_thumbnail.short_description = 'Thumbnail'

    # Customize the list display of product categories.
    list_display = [
        '__str__',
        'title',
        'slug',
        'input_class',
        'display_order',
        'created_at'
    ]

    # Specify the model fields those can be modified from list display page.
    list_editable = ['input_class', 'display_order']

    # Specify read only fields in django web pages for 'Attribute' model.
    readonly_fields = ['admin_thumbnail', 'slug', 'created_at', 'updated_at']

    # Set 'search_fields' to enable a search box on the admin change list page.
    search_fields = ['title']


class PromotionItemInline(nested_admin.NestedTabularInline):
    """Class to show tabular of model info inside another model in admin page
    """

    model = models.PromotionItem
    extra = 0
    min_num = 0


class ProductItemAttributeInline(nested_admin.NestedTabularInline):
    """Class to show nested tabular of model info inside another model in admin
     page"""

    model = models.ProductItemAttribute
    form = forms.ProductItemAttributeInlineForm
    extra = 0
    # Require that at least one value should set.
    min_num = 0
    readonly_fields = ['slug']
    # autocomplete_fields = ['product_attribute']


class ProductItemImageInline(nested_admin.NestedTabularInline):
    """Class to show tabular of model info inside another model in admin page
    """

    model = models.ProductItemImage
    extra = 0
    min_num = 0
    readonly_fields = ['slug', 'created_at', 'updated_at']


class ProductItemAdmin(nested_admin.NestedModelAdmin):
    """Customize variables of your django admin web page for ProductItem
     model"""

    form = forms.ProductItemAdminForm
    inlines = [
        PromotionItemInline,
        ProductItemAttributeInline,
        ProductItemImageInline
    ]
    ordering = ['created_at']
    readonly_fields = [
        'sku',
        'slug',
        'deal_price',
        'category',
        'created_at',
        'updated_at'
    ]
    search_fields = ['__str__']


class ProductItemInline(nested_admin.NestedTabularInline):
    """Class to show nested tabular of model info inside another model in admin
     page"""

    model = models.ProductItem
    inlines = [
        ProductItemAttributeInline,
        PromotionItemInline,
        ProductItemImageInline
    ]
    extra = 0
    min_num = 0
    readonly_fields = ['sku', 'deal_price', 'slug', 'created_at', 'updated_at']


class ProductAttributeInline(nested_admin.NestedTabularInline):
    """Class to show nested tabular of model info inside another model in admin
     page"""

    model = models.ProductAttribute
    form = forms.ProductAttributeInlineForm
    extra = 0
    # Require that at least one value should set.
    min_num = 0
    # readonly_fields = ['slug']
    autocomplete_fields = ['attribute']


class ProductAdmin(nested_admin.NestedModelAdmin):
    """Customize variables of your django admin web page for Product model"""

    form = forms.ProductAdminForm

    admin_thumbnail = AdminThumbnail(image_field=cached_admin_thumb)
    admin_thumbnail.short_description = 'Thumbnail'

    # NOTE: DON't use the class name inside quotes
    inlines = [ProductAttributeInline, ProductItemInline]
    ordering = ['-created_at']
    list_display = [
        'title',
        'product_group',
        'item_list_price',
        'item_deal_price',
        'admin_thumbnail',
        'slug',
        'is_available'
    ]
    list_display_links = ['title']
    readonly_fields = [
        'item_list_price',
        'item_deal_price',
        'slug',
        'created_at',
        'updated_at'
    ]

    # In case wanting to get field value using Foreign Key field.
    # Note: put the method name within your admin model lists to get its value.
    # @admin.display(
    #     ordering='<foreign_key_field>__<field_name>',
    #     description='Brand'
    # )
    # def get_brand(self, obj):
    #     """Return <field_name> value of <foreign_key_field>"""
    #
    #     # check if brand_category is None.
    #     if obj.brand_category:
    #         return obj.<foreign_key_field>.<field_name>


class ReviewAdmin(BaseModelAdmin):
    """Customize variables of your django admin web page for Review model"""

    ordering = ['-created_at']
    list_display = [
        '__str__',
        'is_accepted',
        'created_at',
        'updated_at'
    ]
    list_display_links = ['__str__']
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['__str__', 'is_accepted']


# Change some field that related to Admin site
admin.sites.AdminSite.site_header = 'Jamie & Cassie - Management Console'
admin.sites.AdminSite.site_title = 'Jamie & Cassie'
admin.sites.AdminSite.index_title = 'Jamie & Cassie - Index'

# Note: django.contrib.admin.sites.AlreadyRegistered: The model Site is already
#       registered with 'sites.SiteAdmin', if you want to register custom class
#       first unregister the current one.
admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Meta, MetaAdmin)
admin.site.register(models.Country, CountryAdmin)
admin.site.register(models.Promotion, PromotionAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Banner, BannerAdmin)
admin.site.register(models.TopBanner, TopBannerAdmin)
admin.site.register(models.Card, CardAdmin)
admin.site.register(models.Section, SectionAdmin)
admin.site.register(models.Supplier, SupplierAdmin)
admin.site.register(models.POItem, POItemAdmin)
admin.site.register(models.ShippingMethod, ShippingMethodAdmin)
admin.site.register(models.POShipping, POShippingAdmin)
admin.site.register(models.POProfile, POProfileAdmin)
admin.site.register(models.POPayment, POPaymentAdmin)
admin.site.register(models.Tax, TaxAdmin)
# admin.site.register(models.CountryTax)
admin.site.register(models.PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(models.ProductGroup, ProductGroupAdmin)
admin.site.register(models.Attribute, AttributeAdmin)
admin.site.register(models.ProductItem, ProductItemAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.MetaItem)
admin.site.register(models.Icon)
admin.site.register(models.PaymentMethod)
admin.site.register(models.ProductAttribute)
admin.site.register(models.ProductItemAttribute)
admin.site.register(models.PromotionCategory)
admin.site.register(models.PromotionItem)
admin.site.register(models.Address)
