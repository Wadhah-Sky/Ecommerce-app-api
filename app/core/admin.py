"""Customize and manage your project django admin web page"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.template.defaultfilters import mark_safe
from core import models


class UserAdmin(BaseUserAdmin):
    """Customize variables of your django admin web page"""

    # Override admin web page form-fields specifications.
    formfield_overrides = {
        PhoneNumberField: {
            'widget': PhoneNumberPrefixWidget(initial='IQ'),
            'help_text': _('Choose the country code.'),
            'label':
                _(mark_safe(
                    '<strong style="font-weight: 700; color: var(--body-fg);">'
                    'Phone number</strong>'
                ))
        },
    }

    # Customize the list display order of users in descending.
    ordering = ['-date_joined']

    # Customize the list display of users.
    list_display = ['email', 'first_name', 'last_name', 'username',
                    'last_login', 'date_joined', 'is_active']

    # Customize the links of list display fields.
    list_display_links = ['email', 'first_name', 'last_name', 'username']

    # Specify the sections and fields those will include in 'change' web page
    # for user.
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
                    'first_name', 'last_name', 'username', 'phone_number'
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
                    'last_login', 'date_joined', 'date_modified'
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
                    'first_name', 'last_name', 'username', 'email',
                    'password1', 'password2', 'phone_number'
                )
            }
        ),
    )

    # Specify read only fields in django web pages for 'User' model.
    readonly_fields = (
        'is_superuser', 'last_login', 'date_joined', 'date_modified'
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Category)
