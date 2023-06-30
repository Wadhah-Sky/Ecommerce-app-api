"""Project main models"""

# Note: each python file or any programming script is a module and can have
# sub-module/modules imported in it.
# Python module: A module is a file containing Python definitions and
# statements.
# if you want to split your python code script over multiple files (modules)
# then make sure to create '__init__.py' module (file) to make sure that the
# directory that hold the modules (files) is a module too which will let the
# python interpreter to define him as module and can be imported or reuse it in
# another modules.

# Note: A 'Package' is a directory that consist of multiple directories of
#       modules.
#       in other hand 'Libraries' provide developers with predefined functions
#       and classes defined in modules to make their work easier and boost the
#       development process.
#       while A 'Framework' in programming is a tool consist of multiple
#       packages/libraries that provides ready-made components or solutions
#       that are customized in order to speed up development, so it's like the
#       foundation upon which developers build applications for specific
#       platforms.
#       A computing 'Platform' or 'Digital Platform' is an environment in which
#       a piece of software is executed. It may be the hardware or the
#       operating system (OS), even a web browser and associated application
#       programming interfaces, or other underlying software, as long as the
#       program code is executed with it.

# Info: What the @property decorator does?
#
#       is declaring that the method can be accessed like it's a regular
#       property of the instance.
#       let's assume we have 'full_name()' method in class:
#
#       class User(models.Model):
#
#       first_name = models.CharField(max_length=50)
#       last_name = models.CharField(max_length=50)

#       @property
#       def full_name(self):
#         "Returns the person's full name."
#         return f'{self.first_name, self.last_name}'
#
#
#       This means you can call 'full_name' as if it were a member variable
#       instead of a function, so like this:
#
#       >>person = User()
#       >>person.first_name = 'Ali'
#       >>person.last_name = 'Ahmed'
#
#       >>print(person.full_name)
#
#       Note that we didn't call full_name as function:
#
#       >>print(person.full_name())
#
#       You could also define a setter method in the class 'User' like this:
#
#       @full_name.setter
#       def full_name(self, value):
#          names = value.split(' ')
#          self.first_name = names[0]
#          self.last_name = names[1]
#
#       Using this method, you can set a persons full name like this:
#
#       >>person.full_name = 'John Doe'
#
#       instead of:
#
#       >>person.set_full_name('John Doe')
#
#       If you ever face an error of:
#
#       'NoneType' object is not callable
#
#       OR
#
#       '<property_returned_object>' object is not callable
#
#       This mean your code trying to call the @property function as callable
#       (using parentheses).

# Info: in python 3.10 and later it's possible to do something similar to:
#       switch... case... statement
#
#       by using match... case... statement:
#
#       match term:
#         case pattern-1:
#            action-1
#         case pattern-2:
#            action-2
#         case pattern-3:
#            action-3
#         case _:
#            action-default
#
#        * the _ is default case if none of before cases is true. And no need
#          to set break keyword at each case, it's automatically done by
#          python interpreter.

# Info: To calculate the percentage of certain number:
#
#       (required_percentage)/100 * Number = X

# append() vs += with list in Python?
#
# In general case append will add one item to the list, while += will copy all
# elements of right-hand-side list into the left-hand-side list. so if the
# right-hand-side is a string, then += will add each character of the string
# separately to left-hand-side.

from django import forms
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        BaseUserManager)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.core.validators import MinValueValidator, MaxValueValidator

from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.validators import validate_international_phonenumber

from djmoney.models.fields import MoneyField
from djmoney.money import Money
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator

from imagekit.processors import ResizeToFit, Resize, Thumbnail
from imagekit.models import ProcessedImageField

from django.contrib.postgres import fields as pg_fields

# from colorfield.fields import ColorField

from decimal import Decimal

# from datetime import timedelta

from mptt import models as mptt_models

# import logging
import uuid
import os


# Info: if you want to access details of model fields details e.g. max_length,
#       you have two ways:
#
#       1- <Model_class>._meta.get_field('<field_name>').max_length
#       2- <Model_class>.<field_name>.field.max_length

# Note Postgres has multiple specific fields, like:
#      1- ArrayField: field will accept array of value.
#      2- HStoreField: will accept value of {key:value}, keys should be string,
#         in database stored like this in the cell:
#         Fitted => Relaxing,Manufacture => China
#      3- JSONField: two type(regular and binary).
#      4- CI/Text/Char, means the value will be stored as lowercase, the Text
#         type is unlimited length while the char type is limited with specific
#         size and if you enter value less than specified size the space that
#         left will be padded.
#
#      There multiple options for ArrayFiled:
#
#      1- base_field for postgres ArrayField can be any standard model field
#         except those handling relational data (ForeignKey, OneToOneField and
#         ManyToManyField) and file fields ( FileField and ImageField).
#      2- If you give the field a default, ensure it’s a callable such as list
#         (for an empty default) or a callable that returns a list (such as
#         a function). Incorrectly using default=[] creates a mutable default
#         that is shared between all instances of ArrayField.
#      3- It is possible to nest array fields - you can specify an instance of
#         ArrayField as the base_field.
#      4- size: optional argument, If passed, the array will have a maximum
#         size as specified. This will be passed to the database, When nesting
#         ArrayField, whether you use the size parameter or not, PostgreSQL
#         requires that the arrays are rectangular:
#
#      * Not valid if you set such value:
#        [2, 3],
#        [2],
#
#        Case-insensitive collations:
#        On PostgreSQL 12+, it’s preferable to use non-deterministic collations
#        instead of the 'citext' extension. You can create them using the
#        CreateCollation migration operation.


# How to use Postgres specific fields like (HStoreField, ArrayField)?
# 1- create the extension,
#    A- in django migration file or
#    B- directly into your database using script file to be run whenever your
#       database is starting.
# 2- Add 'django.contrib.postgres' in your INSTALLED_APPS.
#
# You’ll see an error like (can't adapt type 'dict') if you skip the first
# step, or (type "hstore" does not exist) if you skip the second.


# JSONField VS HStore?
#
# 1- HStore is a key value store directly within your database, gives you
#    flexibility when working with your schema, as you don’t have to define
#    models ahead of time. Though its two big limitations are that:
#    1. it's only deals with text
#    2. it's not a full document store meaning you can’t nest objects.
#
# 2- JSON in contrast to HStore is a full document datatype. In addition to
#    nesting objects you have support for more than just text (read numbers).
#    As you insert JSON into Postgres it will automatically ensure its valid
#    JSON and error if its well not


# Note: in Django ORM you have:
#       1- aggregate(): that can be used to aggregate(group) the values of all
#          returned records from the table.
#
#       >>POItem.objects.filter(purchase_order=po_id).aggregate(
#       >>               sum=Sum('total_amount)
#       >>)
#
#       This will return: {'sum': <sum(total_amount) column for all records>}
#
#       OR:
#
#       >><model_class_name>.objects.filter(purchase_order=po_id).aggregate(
#       >>                         Sum('total_amount)
#       >>)
#
#       This will return: <sum(total_amount) column for all records>
#
#       2- annotate(): that can be used to add extra field for every single
#       record been return from the tabel:
#
#       >><model_class_name>.objects.filter(purchase_order=po_id).annotate(
#       >>                         sum=Sum('total_amount)
#       >>)
#
#       This will return for example if we have two records, will add extra
#       field in addition to the fields of the record:
#
#       <QuerySet [{'<first_record_fields>': <their values>,
#                   'sum': Decimal('220.00')},
#                 {'<second_record_fields>': <their values>,
#                   'sum': Decimal('300.00')}]
#       >

# Info: The Decimal() means the type of the field that have summed is Decimal.

# Info: An django ORM F() object represents the value of a model field,
#       transformed value of a model field, or annotated column. It makes it
#       possible to refer to model field values and perform database operations
#       using them without actually having to pull them out of the database
#       into Python memory.
#       Instead, Django uses the F() object to generate an SQL expression that
#       describes the required operation at the database level.

# Info: When using django ORM methods in case the queryset is empty:
#
#       1- .filter(…) method will return empty list.
#       2- .first() and .last() methods will return None.
#       3- .get(), .aearliest(…)/.earliest(…) and .alatest(…)/.latest(…)
#           methods will raise a DoesNotExist exception.

# Info: Django ORM .get(…) method will raise an MultipleObjectsReturned
#       exception if found multiple objects match the lookups values.

# Info: if you are trying to create/delete foreign key records from database
#       table, you need to select the foreign key field value using model
#       instance not an 'id' value.

# Note: You can't make math operations(add, multiply..etc) of Decimal field
#       values directly, you need to use 'decimal.Decimal' class, also you
#       can't use the value of Decimal() in math operation with None type.

# Note: if you use decimal.Decimal with value of models.decimalField the IDE
#       will show a warning:
#
#       Expected type 'Decimal | float | str | tuple[int, Sequence[int], int]',
#       got 'DecimalField' instead
#
#       Ignore this warning. The IDE is making a best guess (from limited
#       information) as to what the data type will be at runtime, but it is
#       guessing wrong. That is, it is fairly reasonable to expect that
#       something multiplied by an int will result in an int if you don't know
#       what that something actually is.
#
#       To solve this warning, add the next comment line above the line causing
#       the warning:
#
#       # noinspection PyTypeChecker

# Info: What difference between only() and values() in django ORM?
#
#       When you use the 'only' method, you still get full Django objects back
#       from the database. These are expensive to set up and take a lot more
#       memory. They actually become almost completely unmanageable when
#       dealing with more than a few thousand items.
#
#       The 'values' method, as you know, puts everything into a standard
#       Python dictionary. These are much harder to work with, but the setup
#       time is trivial and the memory usage is dramatically less.

# Info: When using django ORM methods to return objects from database, the
#       objects could be:
#
#       1- queryset<>, that could be:
#          A- list of objects as dictionaries, like using filter(), values() ..
#          B- one object as dictionary, like using first(), last .. etc if
#             used values() with these methods; whereas will return a model
#             object if not use values().
#       2- model object, like using get() due this function belongs to the
#          Model Manager not to QuerySet class.

# Important: when trying to use validation in model using clean() method, you
#            should know that django will do all clean methods for all
#            instances before start run save method for each instance, so this
#            will cause an issue if you are trying to validate depends on the
#            values of other instances.

# Important: if you ever faced the below error when trying to add/change an
#            instance using django admin webpage:
#
#            SuspiciousFileOperation at <location>
#            Detected path traversal attempt in '<id>.format'
#
#            This probably happen because you made a mistake in the code to
#            manipulate the behavior of save() method, like you do when using
#            signals, for example make a mistake in 'sender' name of @receiver
#            decorator.


# Important: If you want to enforce multiple values input (multiple instances)
#            for a model field using inline class into admin webpage, so to
#            check if the value is duplicate then you can't do it with clean()
#            since each value will check separately and saved in the same time,
#            so the solution is to use:
#
#            constraints = [ models.UniqueConstraint(*options) ]
#
#            inside Meta class of your model.

# Note: In general constraints are not checked during full_clean(), and do not
#       raise ValidationErrors. Rather you’ll get a database integrity error on
#       save(). 'UniqueConstraints' without a condition (i.e. non-partial
#       unique constraints) and expressions (i.e. non-functional unique
#       constraints) are different in this regard, in that they leverage the
#       existing validate_unique() logic, and thus enable two-stage validation.
#       In addition to IntegrityError on save(), ValidationError is also raised
#       during model validation when the UniqueConstraint is violated.

# Note: We don’t usually recommend allowing null=True for CharField since this
#       allows the field to have two “empty values”.

# Note: if you want to make a relation between one model instances with multi
#       instances of another model, use ManyToMany relational, But, if you want
#       to create nested relational like a country has many states and each
#       state has many cities, then you should use reverse relation using
#       Foreign Key (City->Foreign-->State->Foreign-->Country) which called
#       ManyToOne relation, DON'T use ManyToMany relational like:
#       (Country->m2m-->State->m2m-->City) in such cases.

# Note: ForeignKey field, will use the __str__ of the class that connect with,
#       to represent all this class objects in database which trying to connect
#       with them through this field.

# Note: double-underscore, which is used in filter() to separate the
#       field name from the 'lookuptype' or ‘function’, followed by the value
#       to compare to. Per the documentation, the syntax is written like so
#       with following arguments:
#       1- relational-field(in the instance model)
#       2- double-underscore
#       3- lookuptype(in the relational model)
#       4- optional : another double-underscore + function
#       5- =value(looking for)
#
#       ex: filter(field__lookuptype=value)
#       ex: filter(filed__lookuptype__gt=value)
#
#       the second example will use 'gt' function to aggregating and return
#       all objects of 'lookuptype' that have the 'value'.
#
# Note: Many To Many fields are saved after the model instance is saved
#       in database, so, you can't check the that M2M field of instance in
#       clean() using 'self', to do that you need to create a form and define
#       clean() to check the 'cleaned_data' object, then you can this form to
#       your admin related class.

# Note: By setting relational field with both of blank=True and null=True
#       will make it optional to fill.
#       Rather than using ForeignKey field with constraint (unique=True), use
#       OneToOne filed.

# Note: Even though Django takes care of creating the 'through' (intermediate)
#       model on its own and keeps this invisible to a user, sometimes it
#       becomes necessary to use a custom 'through' model in order to add some
#       additional fields to that model.

# Note: if you  need to represent a model instance by using relational filed,
#       which will be represented in ASCII characters form, this will raise an
#       error if used __str__ method to return the relational filed as __str__
#       represent to that instance.
#       So instead can use __unicode__ which will be called by django when it
#       needs to render an object in a context where a string representation is
#       needed (e.g. in the model's admin pages), and this will return the
#       instance in form of object of model.

# Info: By default, Django populates foreign key column's name by appending
#       (_id) to the field name you define in your model. You must explicitly
#       specify column's name using 'db_column' property

# Info: 'MoneyField' is a custom field (Decimal for its amount, Char for its
#       currency) and can't serialize it directly, to return its decimal amount
#       of the field use (amount property) like:
#
#       <money_field_name>.amount
#
#       while its currency stored in different column:
#
#       <money_field_name>_currency
#
#       and can be access using property:
#
#       <money_field_name>.currency
#
#       to store value for MoneyField in database use:
#
#       from djmoney.money import Money
#       <queryset_call>.save(<money_field_name>=Money(<value>,<currency>))
#       <queryset_call>.update(<money_field_name>=Money(<value>,<currency>))

# Info: if you want to use money field, you have multiple options:
#
#       price_per_unit = MoneyField(
#         max_digits=8,
#         decimal_places=2,
#         default_currency='USD',
#         validators=[
#             MinMoneyValidator({'USD': 1, 'IQD': 1000}),
#             MaxMoneyValidator({'USD': 5000, 'IQD': 10000000})
#         ]
#     )

# Info: Any value returned from Money(value, currency) method can be operated
#       with any math operation (multiply, add ..etc), and the operation will
#       return Money value.
#       Also, you can use sorted/sort methods with Money values.


def calculate_discount_amount(amount, discount_percentage):
    """Return the amount of discount"""

    # Calculate the rounded after discount value of the given amount.
    amount_after_discount = round((amount * Decimal(discount_percentage))/100)

    # Return the amount.
    return amount - amount_after_discount


def round_money(amount, currency=settings.MONEY_DEFAULT_CURRENCY,
                round_decimal=settings.MONEY_DECIMAL_PLACES):
    """Method to return Money amount"""

    if amount is not None:
        return Money(round(amount, round_decimal), currency)


def create_image_file_path(instance, filename):
    """Generate file path for a new image"""

    # Info: 'filename' is the name of uploaded image by user.

    # Get the extension from the filename.
    extension = filename.split('.')[-1]

    # Create a new filename to store in the database.
    filename = f'{instance.slug}/{uuid.uuid4()}.{extension}'

    # Get the class name of the given instance.
    # class_name = instance.__class__.__name__.lower()

    # An important SEO (Google search) step that your website brand its
    # uploaded images.
    website_brand_name = 'Jamie-&-Cassie'

    return os.path.join(f'uploads/{website_brand_name}', filename)


def instance_time_stamp(instance):
    """Update time stamp fields for the instance"""

    if not instance.id:
        instance.created_at = timezone.now()

    instance.updated_at = timezone.now()
    return instance


class ISOCode(models.CharField):
    """Customized char field to save its values as lower case"""

    def get_prep_value(self, value):
        """Field class method to perform preliminary non-db specific value
        checks and conversions"""

        return str(value).lower()


class TimeStampedModel(models.Model):
    """Abstract class to create time stamp"""

    # in Django DateTimeField you have three options to set the value of the
    # time:
    # 1- default: which can be set as timezone.now(), this will update the
    #             field value whenever created or updated.
    # 2- auto_now: it updates the field value each time save() method of
    #              instance is triggered.
    # 3- auto_now_add: it updates the field value only when the instance is
    #                  created.
    #
    # Note: if you use any of the above options, the DateTimeField will have
    #       editable=True by default which means this field can be changed by
    #       user unless you set editable=False, another thing to mention when
    #       editable=True, the DateTimeField will be shown in django admin page
    #       by default and editable unless you set this filed in read_only list
    #       in django admin class for the related model.

    # Here we are not using any of the three options.
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        """instruction to use this model as abstract and which means no table
        will be created in the database"""

        abstract = True


class UserManager(BaseUserManager):
    """User model manager"""

    def create_user(self, email, username, password=None, **extra_fields):
        """Creates and save new use"""

        # Note: checking the required fields by model is blank or not, it's
        #       unnecessary because model itself will refuse the blank value.

        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have an username')
        if extra_fields['phone_number']:
            validate_international_phonenumber(extra_fields['phone_number'])

        # create a record.
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password, **extra_fields):
        """Creates and save new superuser"""

        # create a record.
        user = self.create_user(
            email,
            username,
            password,
            **extra_fields
        )

        # Add extra permissions and field values.
        user.is_superuser = True
        user.is_staff = True
        user.role = 'admin'

        # update user object in database with the extra permissions.
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""

    # Specify role field choices.
    role_choices = (
        ("admin", "Admin"),
        ("sales", "Sales"),
        ("inventory", "Inventory"),
        ("customer", "Customer")
    )

    # Define model fields.
    # 'slug' set by signal.
    slug = models.SlugField(max_length=100, unique=True)
    thumbnail = ProcessedImageField(
        blank=True,
        upload_to=create_image_file_path,
        format='JPEG',
        options={'quality': 90},
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = PhoneNumberField(unique=True)
    role = models.CharField(
        max_length=30,
        choices=role_choices,
        default='customer'
    )
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Hook in the custom model manager.
    # 'objects' is the alias name of model default manager, and you use it when
    # do queryset on database tabel e.g. User.objects.get(email=<value>)
    objects = UserManager()

    # Change default username field of user model to be the email field.
    USERNAME_FIELD = 'email'

    # Specify required fields for register a new user using superuser command.
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'phone_number']

    @property
    def full_name(self):
        """Return full name of user by using his first and last name"""

        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        """On save() method call for this model, update timestamps"""

        return super(User, instance_time_stamp(self)).save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        """Returns True if the user has the specified permission"""

        # Where 'perm' is in the format "<backend label>.<permission codename>"
        # If 'obj' is passed in, this method won’t check for a permission for
        # the model, but for this specific object.
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Returns True if the user has any permissions in the given package
        (the Django backend label)"""

        return True

    def __str__(self):
        """String representation of model objects"""

        return self.email


class Meta(models.Model):
    """Model for create meta instances"""

    class Meta:
        """Customize django default way to plural the class name"""

        verbose_name = 'Meta'
        verbose_name_plural = 'Meta'

    # Define model fields.
    title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        """String representation of model objects"""

        return self.title


class MetaItem(models.Model):
    """Model for create meta item instances"""

    class Meta:
        """A Meta-class customization of model"""

        constraints = [
            models.UniqueConstraint(
                fields=['value', 'meta'],
                name='meta_item_unique_appversion'
            ),
        ]

    # Define model fields.
    value = models.CharField(max_length=56, unique=True)
    meta = models.ForeignKey(
        'Meta',
        on_delete=models.CASCADE,
        related_name='meta_items_meta'
    )

    def __str__(self):
        """String representation of model objects"""

        return f'{self.meta.title}, {self.value}'


class Country(models.Model):
    """Model to create country instances"""

    class Meta:
        """Customize django default way to plural the class name"""

        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    # Specify countries choices using 'named groups'.
    #     # 1- (value, "human readable text")
    #     # 2- ("group name", (value, "human readable text") )
    #     country_name_choices = (
    #         ("IRQ", "Iraq"),
    #         ("USA", "United State of America"),
    #         ("United Kingdom", (
    #             ("Scotland", "Scotland"),
    #             ("Great Britain", "Great Britain")
    #         )),
    #     )

    # class Country(models.TextChoices):
    #     """Enumeration class to set choices for country field"""
    #
    #     # Note: Enumeration types do not support 'named groups'.
    #
    #     # You can access the details using (.name, .value, .label)
    #     # Use the bellow formula:
    #     # VAR_NAME = value, _(human readable label)
    #
    #     # Countries
    #     IRAQ = 'IRQ', _('Iraq')

    # Define model fields.
    title = models.CharField(max_length=56, unique=True)
    iso_code = ISOCode(max_length=2, unique=True)
    display_order = models.PositiveSmallIntegerField(default=10)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        """String representation of model objects"""

        return f'{self.title}, {self.iso_code}, available: {self.is_available}'


class Address(models.Model):
    """Model to create address instances"""

    class Meta:
        """Customize django default way to plural the class name"""

        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    # Define model fields.
    # unit_number = models.CharField(max_length=5, blank=True)
    # street_number = models.CharField(max_length=3, blank=True)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=85)
    region = models.CharField(max_length=85)
    postal_code = models.CharField(max_length=8, blank=True)
    country = models.ForeignKey(
        'Country',
        on_delete=models.RESTRICT,
        related_name='Addresses_country'
    )

    def __str__(self):
        """String representation of model objects"""

        address = [
            # self.unit_number,
            # self.street_number,
            self.address_line_1,
            self.city,
            self.country
        ]

        returned_value = []

        for value in address:
            if value:
                returned_value.append(str(value))

        return ", ".join(returned_value)


class UserAddress(models.Model):
    """Model to create user's address instances"""

    # 'UniqueConstraints' expects a list of the fields you’d like to be unique
    # together, and you can add condition to enforce on fields to make sure
    # that fields should verify when add or change them.

    # The options for 'UniqueConstraint' class:
    # UniqueConstraint(*expressions, fields=(), name=None, condition=None,
    #                  deferrable=None, include=None, opclasses=())
    #
    # fields=():
    # Specify the unique set of columns you want the constraint to enforce,
    # so no duplicate data saved when trying to post multiple values to the
    # model database.
    #
    # name=None:
    # The name of the constraint. You must always specify a unique name for
    # each constraint in your entire model file.
    #
    # include=None:
    # A list or tuple of the names of the fields to be included in the covering
    # unique index as non-key columns. This allows index-only scans to be used
    # for queries that select only included fields (include) and filter only by
    # unique fields (fields).

    class Meta:
        """Customize django default way to plural the class name and add
        constraints"""

        verbose_name = 'User Address'
        verbose_name_plural = 'User Addresses'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'address'],
                name='user_address_unique_appversion'
            ),
            models.UniqueConstraint(
                fields=['user'],
                condition=models.Q(is_default=True),
                name='one_default_address_per_user'
            )
        ]

    # Define model fields.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_addresses_user'
    )
    address = models.ForeignKey(
        'Address',
        on_delete=models.CASCADE,
        related_name='user_addresses_address'
    )
    is_default = models.BooleanField(default=False)

    def clean(self):
        """Restrict the add/change to model fields"""

        if self.is_default is True:
            # we exclude current instance in case we are trying to update the
            # data. Not to forget we can't have more than one instance with the
            # same user and address value using 'UniqueConstraint'.
            if UserAddress.objects.filter(
                    user=self.user,
                    is_default=True
            ).exclude(id=self.id).count() >= 1:
                raise forms.ValidationError(
                    "You can't set more than one default address"
                )

    def __str__(self):
        """String representation of model objects"""

        return f'{self.user}, {self.address}'


class Icon(models.Model):
    """Model to create icon instances"""

    title = models.CharField(max_length=30, unique=True)
    class_attribute_value = models.CharField(max_length=40)

    def __str__(self):
        """String representation of model objects"""
        return self.title


class Category(mptt_models.MPTTModel, TimeStampedModel):
    """Model to create product-categories instances using Modified Preorder
    Tree Traversal"""

    # Info: Since MPTTModel inherits from models.Model, this is very important
    #       when you have “diamond-style” multiple inheritance :
    #       you inherit from two Models that both inherit from the same base
    #       class (e.g. models.Model) . In that case, If MPTTModel is not the
    #       first Model, you may get errors at Model validation, like
    #       AttributeError: 'NoneType' object has no attribute 'title'.

    class MPTTMeta:
        """Set metadata for your MPTTModel class"""

        # Note: The available options for the MPTTMeta class are:
        # 1- parent_attr: The name of a field which relates the model back to
        #                 itself such that each instance can be a child of
        #                 another instance. Defaults to 'parent'.
        #
        # * For the following four arguments, if fields with the given names do
        #   not exist, they will be added to the model dynamically:
        # 2- left_attr: The name of a field which contains the left tree node
        #               edge indicator, which should be a
        #               'PositiveIntegerField'. Defaults to 'lft'.
        # 3- right_attr: The name of a field which contains the right tree
        #                node edge indicator, which should be a
        #                'PositiveIntegerField'. Defaults to 'rght'.
        # 4- tree_id_attr: The name of a field which contains the tree id of
        #                  each node, which should be a 'PositiveIntegerField'.
        #                  Defaults to 'tree_id'.
        #                  Items which do not have a parent are considered to
        #                  be “root” nodes in the tree and will be allocated
        #                  a new tree id. All descendants of root nodes will
        #                  be given the same tree id as their root node.
        # 5- level_attr: The name of a field which contains the (zero-based)
        #                level at which an item sits in the tree, which should
        #                be a 'PositiveIntegerField'. Defaults to 'level'.
        #                For example, root nodes would have a level of 0 and
        #                their immediate children would have have a level of
        #                '1'.
        # 6- order_insertion_by: A list of field names which should define
        #                        ordering when new tree nodes are being
        #                        inserted or existing nodes are being
        #                        re-parented, with the most significant
        #                        ordering field name first. Defaults to [].
        #                        It is assumed that any field identified as
        #                        defining ordering will never be NULL in the
        #                        database. This will require an extra database
        #                        query to determine where nodes should be
        #                        positioned when they are being saved. This
        #                        option is handy if you’re maintaining mostly
        #                        static structures, such as trees of
        #                        categories, which should always be in
        #                        alphabetical order.

        # order_insertion_by = ['category_name']

    class Meta:
        """Set metadata for your Model class"""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        constraints = [
            models.UniqueConstraint(
                fields=['parent', 'title'],
                name='category_unique_appversion'
            )
        ]

    # Define model fields.
    # 'slug' set by signal.
    slug = models.SlugField(max_length=100, unique=True)
    thumbnail = ProcessedImageField(
        blank=True,
        upload_to=create_image_file_path,
        processors=[ResizeToFit(70, 70)],
        format='JPEG',
        options={'quality': 100}
    )
    # Note: implement hierarchy of categories using self joining concept.
    # Info: 'TreeOneToOneField', is just a regular 'OneToOneField' that renders
    #       form fields differently in the admin and a few others places.
    # Info: You can’t use a many-to-many as your ‘parent’ field. That’s because
    #       the mptt algorithm only handles trees, not arbitrary graphs. A tree
    #       where nodes can have multiple parents isn’t really a tree at all.
    parent = mptt_models.TreeForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='leaf_nodes'
    )
    title = models.CharField(max_length=30)
    display_order = models.PositiveSmallIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    icon = models.ForeignKey(
        'Icon',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='product_categories_icon'
    )

    def clean(self):
        """Restrict the add/change to model fields"""

        # the fields that defined in class 'mptt' can't be clean if it's not
        # define in your model, it will be None in your model clean() method at
        # add time (Not at change time).

        # if self.display_order is not None:
        #     # we exclude current instance in case we are trying to update the
        #     # data.
        #     if Category.objects.filter(
        #             parent=self.parent,
        #             display_order=self.display_order
        #     ).exclude(id=self.id).count() >= 1:
        #         raise forms.ValidationError(
        #             {
        #                 'display_order': "You can't set same display order "
        #                                  "to more than one object those in "
        #                                  "the same level of same tree"
        #             }
        #         )
        if self.parent is None:
            if Category.objects.filter(
                    title=self.title
            ).exclude(id=self.id).count() >= 1:
                raise forms.ValidationError(
                    {
                        'title': "You already have root node with same "
                                 "category title"
                    }
                )

    def save(self, *args, **kwargs):
        """On save() method call for this model, update timestamps"""

        return super(
            Category,
            instance_time_stamp(self)
        ).save(*args, **kwargs)

    def __str__(self):
        """String representation of model objects"""

        full_path = [self.title]
        next_category = self.parent
        while next_category is not None:
            full_path.append(next_category.title)
            next_category = next_category.parent

        # return the list as string in reverse order.
        # Note: Python sequence slice addresses can be written as
        #       list_name[start:end:step] and any of start, stop or end can be
        #       dropped.
        #       list_name[::3] is every third element of the sequence
        #       (jumping), or can be used to print a list in reverse order.
        return ' / '.join(full_path[::-1])


class Promotion(TimeStampedModel):
    """Model to create promotion instances"""

    # Specify promotion_type field choices.
    promotion_type_choices = (
        ("Deal", "Deal"),
        ("Coupon", "Coupon")
    )

    # Set your custom validators.
    PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

    # Define model fields.
    title = models.CharField(
        max_length=12,
        unique=True,
        help_text="Can be use as coupon code, on frontend it is contained "
                  "inside red colored block"
    )
    summary = models.TextField(
        max_length=21,
        blank=True,
        help_text="on frontend it is contained inside white colored block next"
                  " to title promotion block"
    )
    discount_percentage = models.DecimalField(
        max_digits=3,
        decimal_places=0,
        validators=PERCENTAGE_VALIDATOR,
        default='0',
        help_text="%"
    )
    promotion_type = models.CharField(
        max_length=12,
        choices=promotion_type_choices,
        default='Deal'
    )
    max_use_times = models.PositiveIntegerField(default=10)
    used_times = models.PositiveIntegerField(default=0)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    # You can enter a duration with a string with following format:
    # [DD] [[hh:]mm:]ss
    # duration = models.DurationField(
    #     default=timedelta(minutes=20),
    #     help_text="Set the duration time ([DD] [[hh:]mm:]ss) for the"
    #               " promotion"
    # )
    unlimited_use = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    @property
    def duration(self):
        """Combine start_date with duration time"""

        # Return end_date by add duration time into start_date.
        # Ignore the warning of:
        #
        # Class 'DateTimeField' does not define '__sub__'
        #
        # Because we set the start_date field to use timezone() value.
        return self.end_date - self.start_date

    @property
    def promotion_status(self):
        """Return the status of promotion depending on start and end date"""

        # In case the current time is less than start date.
        if timezone.now() < self.start_date:
            return "Not started yet"
        # In case the current time is bigger than end date.
        elif timezone.now() > self.end_date:
            return "Expired"
        # Otherwise the promotion is active.
        else:
            return "Active"

    def clean(self):
        """Restrict the add/change to model fields"""

        if self.end_date < self.start_date:
            raise forms.ValidationError(
                {
                    'end_date': "You can't set the end date less than the"
                                " start date"
                }
            )

    def save(self, *args, **kwargs):
        """On save() method call for this model, update timestamps"""

        return super(
            Promotion,
            instance_time_stamp(self)
        ).save(*args, **kwargs)

    def __str__(self):
        """String representation of model objects"""

        return f'{self.title}, {self.discount_percentage}%,' \
               f' Duration time: {self.duration}, Active: {self.is_active},' \
               f' Status: {self.promotion_status}'


class PromotionCategory(models.Model):
    """Model class to set promotion with category"""

    class Meta:
        """Set metadata for your Model class"""

        verbose_name = 'Promotion Category'
        verbose_name_plural = 'Promotion Categories'
        constraints = [
            models.UniqueConstraint(
                fields=['promotion', 'category'],
                name='promotion_category_unique_appversion'
            )
        ]

    # Define model fields.
    promotion = models.ForeignKey(
        'Promotion',
        on_delete=models.CASCADE,
        related_name='promotion_categories_promotion',
        help_text="Make sure the selected promotion will be used only for the"
                  " selected category, so, when you delete this promotion will"
                  " be deleted from products items too without issue"
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='promotion_categories_category'
    )

    def __str__(self):
        """String representation of model objects"""
        return f'{self.promotion}, {self.category}'


class Banner(TimeStampedModel):
    """Model to create banner objects"""

    # Define model fields.
    # 'slug' set by signal.
    slug = models.SlugField(max_length=100)
    thumbnail = ProcessedImageField(
        upload_to=create_image_file_path,
        format='JPEG',
        options={'quality': 100},
        processors=[Resize(1118, 280)]
    )
    title = models.CharField(max_length=40, unique=True)
    frontend_path = models.CharField(max_length=200, blank=True)
    display_order = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        unique=True
    )
    is_active = models.BooleanField(default=False)

    def clean(self):
        """Restrict the add/change to model fields"""

        if self.is_active:
            # in case trying to change (update) an instance, exclude the
            # current instance from counting.
            if Banner.objects.filter(is_active=True).exclude(
                    id=self.id).count() >= 6:
                raise forms.ValidationError(
                    {
                        'is_active': "You can't set more than 6 active banners"
                    }
                )

    def save(self, *args, **kwargs):
        """On save() method call for this model, update timestamps"""

        return super(
            Banner,
            instance_time_stamp(self)
        ).save(*args, **kwargs)

    def __str__(self):
        """String representation of model objects"""
        return self.title


class Section(TimeStampedModel):
    """Model to create section instances"""

    # Define model fields.
    title = models.CharField(max_length=30, unique=True)
    display_order = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        unique=True
    )
    is_active = models.BooleanField(default=False)

    def clean(self, *args, **kwargs):
        """Restrict the add/change to model fields"""

        if self.is_active:
            if Section.objects.filter(is_active=True).exclude(
                    id=self.id).count() >= 3:
                raise forms.ValidationError(
                    {
                        'is_active': "You can't set more than 3 sections as "
                                     "active"
                    }
                )

    def save(self, *args, **kwargs):
        """On save() method call for this model, update timestamps"""

        return super(
            Section,
            instance_time_stamp(self)
        ).save(*args, **kwargs)

    def __str__(self):
        """Unicode representation of model objects"""

        return self.title


class Card(TimeStampedModel):
    """Model to create card objects to be used by 'Section' model class"""

    # 'CheckConstraint' creates a check constraint in the database, to ensures
    # that given rules are met before a new model object is created.

    # The options for 'CheckConstraint' class:
    # CheckConstraint(*, check, name)
    #
    # check=:
    # A Q object or boolean Expression (models.Exists()) that specifies the
    # check you want the constraint to enforce.
    #
    # name=:
    # The name of the constraint. You must always specify a unique name for the
    # constraint.

    # Q class create objects to represent an SQL condition which can be used in
    # database-related operations.

    # NOTE: 'CheckConstraint' will rise 'IntegrityError' when the data trying
    #        to add/update to database model is not verify the constraint, so,
    #        for better user experience you need to write own form validation
    #        through clean() method.

    # class Meta:
    #
    #     constraints = [
    #         models.CheckConstraint(
    #             check=(
    #                  models.Q(title__isnull=False)
    #             ),
    #             name="card_fill"
    #         )
    #     ]

    # Define model fields.
    # uuid = models.UUIDField(
    #     db_index=True,
    #     default=uuid.uuid4,
    #     editable=False
    # )
    slug = models.SlugField(max_length=100)
    # processors=[ResizeToFit(220, 221)]
    thumbnail = ProcessedImageField(
        upload_to=create_image_file_path,
        format='JPEG',
        options={'quality': 100},
        processors=[ResizeToFit(220, 221)]
    )
    title = models.CharField(max_length=40)
    summary = models.TextField(max_length=150)
    frontend_link_text = models.CharField(max_length=25, default="Shop now")
    category = models.ForeignKey(
        'Category',
        # to_field='slug',
        # db_column='category_slug',
        on_delete=models.CASCADE,
        related_name='cards_category'
    )

    def save(self, *args, **kwargs):
        """On save() method call for this model, update timestamps"""

        return super(
            Card,
            instance_time_stamp(self)
        ).save(*args, **kwargs)

    def __str__(self):
        """String representation of model objects"""

        # Note: 'category_slug' will be represented by its str() method not by
        #       its actual value stored in 'Card' table.
        return f'{self.category}, {self.title}'


class SectionCard(models.Model):
    """Model to create icon instances"""

    class Meta:
        """Set metadata for your Model class"""

        constraints = [
            models.UniqueConstraint(
                fields=['section', 'card'],
                name='section_card_unique_appversion'
            )
        ]

    # Define model fields.
    section = models.ForeignKey(
        'Section',
        on_delete=models.CASCADE,
        related_name='section_cards_section'
    )
    card = models.ForeignKey(
        'Card',
        on_delete=models.CASCADE,
        related_name='section_cards_card'
    )

    def clean(self):
        """Restrict the add/change to model fields"""

        if SectionCard.objects.filter(section=self.section).exclude(
                id=self.id).count() >= 4:
            raise forms.ValidationError(
                    "You can't set more than 4 cards for each section"
                )

    def __str__(self):
        """String representation of model objects"""

        return f'{self.section}, {self.card}'


class Supplier(TimeStampedModel):
    """Model class to for supplier instances"""

    # Define model fields.
    uuid = models.UUIDField(
        db_index=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, blank=True)
    phone_number = PhoneNumberField()
    contact_name = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        """On save() method call for this model, update timestamps"""

        return super(
            Supplier,
            instance_time_stamp(self)
        ).save(*args, **kwargs)

    def __str__(self):
        """String representation of model objects"""
        return f'{self.title}, {self.contact_name}'


class SupplierAddress(models.Model):
    """Model to create supplier's address instances"""

    class Meta:
        """Set metadata for your Model class"""

        verbose_name = 'Supplier Address'
        verbose_name_plural = 'Supplier Addresses'
        constraints = [
            models.UniqueConstraint(
                fields=['supplier', 'address'],
                name='supplier_address_unique_appversion'
            ),
            models.UniqueConstraint(
                fields=['supplier'],
                condition=models.Q(is_default=True),
                name='one_default_address_per_supplier'
            )
        ]

    # Define model fields.
    supplier = models.ForeignKey(
        'Supplier',
        on_delete=models.CASCADE,
        related_name='supplier_addresses_supplier'
    )
    address = models.ForeignKey(
        'Address',
        on_delete=models.CASCADE,
        related_name='supplier_addresses_address'
    )
    is_default = models.BooleanField(default=False)

    def clean(self, *args, **kwargs):
        """Restrict the add/change to model fields"""

        if self.is_default is True:
            if SupplierAddress.objects.filter(
                    supplier=self.supplier,
                    is_default=True
            ).exclude(id=self.id).count() >= 1:
                raise forms.ValidationError(
                    {
                        "is_default": "You can't set more than one default "
                                      "address"
                    }
                )

    def __str__(self):
        """String representation of model objects"""

        return f'{self.supplier}, {self.address}'


class ShippingMethod(models.Model):
    """Model class for create shipping method instances"""

    # Define model fields.
    title = models.CharField(max_length=20, unique=True)
    contact_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        """Validate 'phone number' if provided"""

        if self.phone_number:
            validate_international_phonenumber(self.phone_number)
        if self.email:
            self.email = BaseUserManager.normalize_email(self.email)

        return super(
            ShippingMethod,
            instance_time_stamp(self)
        ).save(*args, **kwargs)

    def __str__(self):
        """String representation of model objects"""
        return self.title


class POShipping(TimeStampedModel):
    """Model class for create purchase order shipping instances"""

    # Set your custom validators.
    MONEY_VALIDATOR = [
        MinMoneyValidator({'USD': 0}),
    ]

    class Meta:
        """Set metadata for your Model class"""

        constraints = [
            models.UniqueConstraint(
                fields=['shipping_method', 'address'],
                name='po_shipping_unique_appversion'
            ),
        ]

    # Define model fields.
    shipping_method = models.ForeignKey(
        'ShippingMethod',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='po_shipping_shipping_method'
    )

    address = models.ForeignKey(
        'Address',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='po_shipping_address'
    )

    cost = MoneyField(
        max_digits=8,
        decimal_places=settings.MONEY_DECIMAL_PLACES,
        default_currency=settings.MONEY_DEFAULT_CURRENCY,
        validators=MONEY_VALIDATOR
    )

    def save(self, *args, **kwargs):
        """On save() method call for this model, update timestamps"""

        return super(
            POShipping,
            instance_time_stamp(self)
        ).save(*args, **kwargs)

    def __str__(self):
        """String representation of model objects"""

        shipping = [
            self.shipping_method,
            self.address,
            self.cost
        ]

        returned_value = []

        for value in shipping:
            if value:
                returned_value.append(str(value))

        return ", ".join(returned_value)


class POProfileManager(models.Manager):
    """Custom manager for POProfile model"""

    def create(self, *args, **kwargs):
        """Override the create method of Manager queryset"""

        if kwargs['phone_number']:
            validate_international_phonenumber(kwargs['phone_number'])
        if kwargs['email']:
            kwargs['email'] = BaseUserManager.normalize_email(kwargs['email'])

        return super(POProfileManager, self).create(*args, **kwargs)


class POProfile(TimeStampedModel):
    """Model class for create purchase order profile instances"""

    # Note: if you want to change the name of default model mager:
    #
    #       profiles = models.Manager()
    #
    #       now the default manager is named as 'profiles'

    # Note: if you are using multiple manager objects in same model then you
    #       need to be careful about the order of the manager objects defined.
    #       The first defined manager object will be treated as default manager
    #       object. For example – In above example, “profiles” is the default
    #       manager as it is defined first. Django uses default managers in
    #       some internal process. So, be careful about choosing your default
    #       manager, or you may get some unexpected results. If you want to
    #       make a manager default and that manager object is not defined first
    #       then you can define it as default manager by setting:
    #
    #       class Meta:
    #            default_manager_name = <value>
    #

    # Info: A “Client” is someone who uses your services on one or more
    #       occasions, while the “Customer” is someone who purchases from your
    #       business on a recurring basis.

    # Define model fields.
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = PhoneNumberField(unique=True)
    role = models.CharField(max_length=30, default='client')

    # Hook in the custom model manager.
    # 'objects' is the alias name of model default manager, and you use it when
    # do queryset on database tabel e.g. POProfile.objects.get(email=<value>)
    objects = POProfileManager()

    @property
    def full_name(self):
        """Returns the person's full name."""

        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        """On save() method call for this model, update timestamps"""

        return super(
            POProfile,
            instance_time_stamp(self)
        ).save(*args, **kwargs)

    def __str__(self):
        """String representation of model objects"""
        return f'{self.full_name}, {self.email}'


class PaymentMethod(models.Model):
    """Model class for create payment method instances"""

    # Define model fields.
    title = models.CharField(max_length=20, unique=True)
    is_card = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    icon = models.ForeignKey(
        'Icon',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='payment_methods_icon'
    )
    icon_color = models.CharField(max_length=6, default='0F1111')

    def __str__(self):
        """String representation of model objects"""
        return f'{self.title}'


class POPayment(TimeStampedModel):
    """Model class for create purchase order payment instances"""

    # Define model fields.
    uuid = models.UUIDField(
        db_index=True,
        default=uuid.uuid4,
        editable=False
    )
    # 'Provider' means the issuer of card e.g. bank.
    provider = models.CharField(max_length=50, blank=True)
    card_number = models.IntegerField(null=True, blank=True)
    cardholder_name = models.CharField(max_length=50, blank=True)
    expiry_date = models.DateField(blank=True, null=True)
    payment_method = models.ForeignKey(
        'PaymentMethod',
        on_delete=models.RESTRICT,
        related_name='po_payments_payment_method'
    )
    # Billing address
    address = models.ForeignKey(
        'Address',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='po_payments_address'
    )
    use_shipping_address = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        """On save() method call for this model, update timestamps"""

        return super(
            POPayment,
            instance_time_stamp(self)
        ).save(*args, **kwargs)

    def __str__(self):
        """String representation of model objects"""

        payment = [
            self.provider,
            self.card_number,
            self.cardholder_name,
            self.expiry_date,
            self.payment_method
        ]

        returned_value = []

        for value in payment:
            if value:
                returned_value.append(str(value))

        return ", ".join(returned_value)


class Tax(TimeStampedModel):
    """Model class for create tax instances"""

    # Specify tax fulfill field choices.
    TAX_FULFILL_CHOICES = (
        ("after discount", "After discount"),
        ("before discount", "Before discount")
    )

    # Set your custom validators.
    PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

    # Define model fields.
    title = models.CharField(max_length=30, unique=True)
    tax_percentage = models.DecimalField(
        max_digits=3,
        decimal_places=0,
        validators=PERCENTAGE_VALIDATOR,
        default='0',
        help_text="Set tax percentage (0-100)"
    )
    tax_fulfill = models.CharField(
        max_length=20,
        choices=TAX_FULFILL_CHOICES,
        default='after discount'
    )

    def save(self, *args, **kwargs):
        """On save() method call for this model, update timestamps"""

        return super(
            Tax,
            instance_time_stamp(self)
        ).save(*args, **kwargs)

    def __str__(self):
        """String representation of model objects"""
        return f'{self.title}, {self.tax_percentage}%, {self.tax_fulfill}'


# class CountryTax(models.Model):
#     """Model class for create country tax instance"""
#
#     class Meta:
#         """Set metadata for your Model class"""
#
#         verbose_name = 'Country tax'
#         verbose_name_plural = 'Country taxes'
#
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['country', 'tax'],
#                 name='country_tax_unique_appversion'
#             ),
#         ]
#
#     # Define model fields.
#     country = models.ForeignKey(
#         'Country',
#         on_delete=models.CASCADE,
#         related_name='country_tax_country'
#     )
#     tax = models.ForeignKey(
#         'Tax',
#         on_delete=models.CASCADE,
#         related_name='country_tax_tax'
#     )
#     is_customer_tax = models.BooleanField(default=False)
#
#     def __str__(self):
#         """String representation of model objects"""
#         return f'{self.country.title}, {self.tax.title}'


class POStatus(models.Model):
    """Model class for create purchase order status instances"""

    # Specify PO status field choices.
    PO_STATUS_CHOICES = (
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("returned", "Returned"),
        ("canceled", "canceled")
    )

    # Define model fields.
    title = models.CharField(
        max_length=20,
        choices=PO_STATUS_CHOICES,
        default='Processing'
    )

    def __str__(self):
        """String representation of model objects"""
        return self.title


class PurchaseOrder(TimeStampedModel):
    """Model class for create purchase order instances"""

    # Define model fields.
    # 'po_code' set by signal.
    po_code = models.CharField(max_length=50, verbose_name='PO code')
    summary = models.TextField(max_length=255, blank=True)
    po_profile = models.ForeignKey(
        'POProfile',
        on_delete=models.PROTECT,
        related_name='purchase_orders_po_profile'
    )
    po_payment = models.ForeignKey(
        'POPayment',
        on_delete=models.PROTECT,
        related_name='purchase_orders_po_payment'
    )
    promotion = models.ForeignKey(
        'Promotion',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='purchase_orders_promotion'
    )
    tax = models.ForeignKey(
        'Tax',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='purchase_orders_tax'
    )
    po_shipping = models.ForeignKey(
        'POShipping',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='purchase_orders_po_shipping'
    )
    supplier = models.ForeignKey(
        'Supplier',
        on_delete=models.PROTECT,
        related_name='purchase_orders_supplier'
    )
    po_status = models.ForeignKey(
        'POStatus',
        on_delete=models.PROTECT,
        related_name='purchase_orders_po_status'
    )

    @property
    def po_status_title(self):
        """Return the title of purchase order status"""
        return self.po_status.title

    @property
    def po_discount_percentage(self):
        """Return the decimal discount percentage of promotion if exist"""

        if self.promotion:
            return self.promotion.discount_percentage

    @property
    def po_tax_fulfill(self):
        """Return tax fulfill"""
        if self.tax:
            return self.tax.tax_fulfill

    @property
    def po_tax_percentage(self):
        """Return tax percentage"""
        if self.tax:
            return self.tax.tax_percentage

    @property
    def subtotal(self):
        """Calculate the total payable amount money of the order items without
        discount"""

        # Get the sum of total amount of all POItem instances those related
        # to this PO instance.

        # Note: you can use django ORM method values('') to specify the
        #       fields(columns) will be selected and return the object as
        #       dictionary.

        # Info: for below queryset call it's unnecessary to use all() method.
        queryset = self.po_items_purchase_order.values(
            'price_per_unit',
            'quantity'
        ).aggregate(
            sum=models.Sum(models.F('price_per_unit') * models.F('quantity'))
        )

        # Our queryset call will return one object as dictionary not a list.
        if queryset:
            return round_money(queryset['sum'])
        else:
            return round_money(0)

    @property
    def savings(self):
        """Calculate the total discount money of product items those related to
        promotion instance"""

        # Note: You can't make math operations(add, multiply..etc) of Decimal
        #       field values directly, you need to use 'decimal.Decimal' class,
        #       also you can't use the value of Decimal() in math operation
        #       with None type.

        # Initialize discount amount
        discount = round_money(0)

        if self.promotion:

            discount_percentage = self.po_discount_percentage

            po_items = self.po_items_purchase_order.all()

            for item in po_items:

                # Get the promotion item instance.
                promotion_item = PromotionItem.objects.filter(
                    promotion=self.promotion,
                    product_item=item.product_item
                ).first()

                # If promotion item instance is not None.
                if promotion_item:

                    item_price_amount = item.price_per_unit.amount

                    # Get amount after discount for the item price.
                    amount_after_discount = calculate_discount_amount(
                        amount=item_price_amount,
                        discount_percentage=discount_percentage
                    )

                    # Find the discount amount:
                    # price amount minus amount after discount.
                    discount_amount = item_price_amount - amount_after_discount

                    # Add rounded money amount of 'discount amount' multiplied
                    # by the requested quantity value into 'discount'.
                    discount += round_money(
                        amount=discount_amount * item.quantity
                    )

        return discount

    @property
    def po_tax(self):
        """Calculate the tax money in depend on tax_fulfill value"""

        # Note: 1- In case the tax calculated before discount, set the whole
        #          purchase order amount.
        #       2- In case the tax calculated after discount. set the purchase
        #          order amount minus discount.

        tax = 0

        if self.tax:

            subtotal = self.subtotal

            if self.po_tax_fulfill == 'after discount':

                # Minus the purchase order discount money from the subtotal.
                subtotal -= self.savings

            tax = (subtotal.amount * Decimal(self.po_tax_percentage)) / 100

        return round_money(tax)

    @property
    def shipping_cost(self):
        """Return the shipping cost"""

        if self.po_shipping:
            return self.po_shipping.cost

        return round_money(0)

    @property
    def grand_total(self):
        """Return the total amount money for current purchase order instance
        after taking out the discount and then add tax plus shipping cost"""

        return (self.subtotal-self.savings) + self.po_tax + self.shipping_cost

    def save(self, *args, **kwargs):
        """On save() method call for this model, update timestamps"""

        return super(
            PurchaseOrder,
            instance_time_stamp(self)
        ).save(*args, **kwargs)

    def __str__(self):
        """String representation of model objects"""
        return f'{self.po_code}, {self.supplier}, {self.po_status}'


class ProductGroup(TimeStampedModel):
    """Model to create product groups"""

    # Define model fields.
    title = models.CharField(max_length=25, unique=True)
    display_order = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        unique=True
    )
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """On save() method call for this model, update timestamps"""

        return super(
            ProductGroup,
            instance_time_stamp(self)
        ).save(*args, **kwargs)

    def __str__(self):
        """String representation of model objects"""
        return self.title


class Product(TimeStampedModel):
    """Model class to create product instances"""

    class Meta:
        """Set metadata for your Model class"""

        # You can set uniqueness on field index rather than set (unique=True)
        # on the field.
        # indexes field accept list of values.
        # indexes = [CaseInsensitiveUniqueIndex(fields=['title'])]

    # Define model fields.
    slug = models.SlugField(max_length=100)
    thumbnail = ProcessedImageField(
        upload_to=create_image_file_path,
        format='JPEG',
        options={'quality': 100}
    )
    # For frontend store, we set max length be 87 characters.
    title = models.TextField(max_length=100, unique=True)
    summary = models.TextField(max_length=400)
    # You can't set unique constraint on HstoreField since it's {key: value}.
    details = pg_fields.HStoreField(null=True, blank=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='products_category'
    )
    product_group = models.ForeignKey(
        'ProductGroup',
        # to_field='title',
        # db_column='product_group_title',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products_product_group'
    )
    use_item_attribute_img = models.BooleanField(default=False)
    use_item_attribute_color_shape = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)

    def item_instance(self, item=None):
        """Return specific item product if:

         1- item has provided or
         2- the first item that have (is_default=True) or
         3- the last ordered item by 'pk' (default behavior of last() method).
         """

        # You can use first() method to return first model instance of filter
        # from database and not a list of model instance/instances.
        if item:
            try:
                item_instance = self.product_items_product.get(pk=item.pk)

            except ObjectDoesNotExist:
                return None

            # Return item instance if exists.
            return item_instance

        else:
            # In case 'item' None, return the item that has 'is_default=True'
            # or in case no result returned, the last ordered item by 'pk'.
            try:
                item_instance = self.product_items_product.filter(
                    is_default=True
                ).first() or self.product_items_product.last()

            except ObjectDoesNotExist:
                # In case product don't have any related items.
                return None

            # Return item instance if exists
            return item_instance

    def item_list_price(self, item=None):
        """Return the product's item list price"""

        instance = self.item_instance(item=item)
        if instance:
            return instance.list_price

    def item_deal_price(self, item=None):
        """Return the product's item deal price"""

        instance = self.item_instance(item=item)
        if instance:
            return instance.deal_price

    def item_deal_promotion_title(self, item=None):
        """Return the product's item promotion title"""

        instance = self.item_instance(item=item)
        if instance:
            return instance.latest_deal_promotion_item_title

    def item_deal_promotion_summary(self, item=None):
        """Return the product's item promotion summary"""

        instance = self.item_instance(item=item)
        if instance:
            return instance.latest_deal_promotion_item_summary

    def price_currency_symbol(self, item=None):
        """Return the default product's item price currency symbol"""

        instance = self.item_instance(item=item)
        if instance:
            return instance.price_currency_symbol

    @property
    def attributes(self):
        """Return related attribute instances that this product connect with"""

        # Get the related product attribute instances.
        product_attributes = self.product_attributes_product.distinct()

        # Get the attribute instances that related to specific product
        # attribute instances.
        attributes = Attribute.objects.filter(
            product_attributes_attribute__in=product_attributes
        )
        return attributes

    def save(self, *args, **kwargs):
        """On save() method call for this model, update timestamps"""

        return super(Product, instance_time_stamp(self)).save(*args, **kwargs)

    def __str__(self):
        """String representation of model objects"""
        return f'{self.category} / {self.title}'


class ProductItem(TimeStampedModel):
    """Model class to create product's item instances"""

    # Set max and min prices amount, it's useful in filtering to set conditions
    USD_MIN_PRICE_AMOUNT = 0
    USD_MAX_PRICE_AMOUNT = 5000

    # Set your custom validators.
    MONEY_VALIDATOR = [
        MinMoneyValidator({'USD': 1}),
        MaxMoneyValidator({'USD': 5000})
    ]

    class Meta:
        """Set metadata for your Model class"""

        constraints = [
            models.UniqueConstraint(
                fields=['product'],
                condition=models.Q(is_default=True),
                name='one_default_item_per_product'
            ),
            # This constraint can't be use, since the value of stock is
            # changeable.
            # models.CheckConstraint(
            #     check=models.Q(limit_per_order__lte=models.F('stock')),
            #     name='limit_per_order_lte_stock'
            # )
        ]

    # Define model fields.
    # 'slug' set by signal.
    slug = models.SlugField(max_length=100)
    thumbnail = ProcessedImageField(
        blank=True,
        upload_to=create_image_file_path,
        format='JPEG',
        options={'quality': 100}
    )
    sku = models.CharField(max_length=12, unique=True)
    list_price = MoneyField(
        max_digits=8,
        decimal_places=settings.MONEY_DECIMAL_PLACES,
        default_currency=settings.MONEY_DEFAULT_CURRENCY,
        validators=MONEY_VALIDATOR
    )
    stock = models.PositiveSmallIntegerField(default=10)
    # 'limit_per_order' set by signal.
    limit_per_order = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)]
    )
    # You can't set unique constraint on HstoreField since it's {key: value}.
    details = pg_fields.HStoreField(null=True, blank=True)
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='product_items_product'
    )
    supplier = models.ForeignKey(
        'Supplier',
        on_delete=models.PROTECT,
        related_name='product_items_supplier'
    )
    is_default = models.BooleanField(
        default=False,
        help_text="You should set at least one True value and no more than one"
    )

    @property
    def latest_deal_promotion_item_instance(self):
        """Return the latest product item's promotion item instance that its
        type is 'Deal' and still valid"""

        # Queryset to get the latest conditional promotion object related to
        # this instance.
        try:
            promotion_item = self.promotion_items_product_item.filter(
                models.Q(
                    promotion__promotion_type='Deal',
                    promotion__is_active=True,
                    promotion__unlimited_use=True,
                    promotion__start_date__lte=timezone.now(),
                    promotion__end_date__gt=timezone.now()
                ) |
                models.Q(
                    promotion__promotion_type='Deal',
                    promotion__is_active=True,
                    promotion__unlimited_use=False,
                    promotion__used_times__lt=models.F(
                        'promotion__max_use_times'
                    ),
                    promotion__start_date__lte=timezone.now(),
                    promotion__end_date__gt=timezone.now()
                )
            ).distinct().latest('pk')

        except ObjectDoesNotExist:
            # latest() will throw an exception if it doesn't return an object.
            return None
        else:
            return promotion_item

    @property
    def latest_deal_promotion_item_title(self):
        """Return the title of promotion for latest deal promotion item"""

        # Get the latest deal promotion item instance.
        instance = self.latest_deal_promotion_item_instance

        # Check if the return object is not None.
        if instance:
            return instance.promotion.title

    @property
    def latest_deal_promotion_item_summary(self):
        """Return the summary of promotion for latest deal promotion item"""

        # Get the latest deal promotion item instance.
        instance = self.latest_deal_promotion_item_instance

        # Check if the return object is not None.
        if instance:
            return instance.promotion.summary

    @property
    def deal_price(self):
        """Calculate the deal price for this product item instance"""

        # You can round number to closet integer without decimal value using
        # round() method.

        # Get the latest deal promotion item instance.
        instance = self.latest_deal_promotion_item_instance

        # Check if the return object is not None.
        if instance:

            ########################################################
            # This block to return deal price while counting the decimal value
            # of list price.
            ########################################################

            # Calculate the required percentage for list_price.
            # required_percentage = round(
            #     100 - Decimal(instance.promotion.discount_percentage)
            # )
            #
            # Return the deal_price as Money value.
            # return round_money(
            #     (Decimal(
            #         required_percentage / 100
            #     ) * self.list_price.amount),
            #     self.list_price.currency
            # )
            #######################################################

            #######################################################
            # This block of code to return deal price while keeping the
            # decimal value of list price.
            #######################################################

            # Get the list price amount.
            amount = self.list_price.amount

            # Get the discount percentage of promotion.
            discount_percentage = instance.promotion.discount_percentage

            # Get the calculated amount of discount.
            deal_price_amount = calculate_discount_amount(
                amount=amount,
                discount_percentage=discount_percentage
            )

            # Return the deal_price as Money value.
            return round_money(deal_price_amount, self.list_price.currency)
            ########################################################

    @property
    def price_currency_symbol(self):
        """Change format of money field currency from ISO to specific symbol"""

        # Get currency object (dictionary) of list_price and convert the code
        # of currency to corresponding currency symbol.
        return settings.CURRENCY_SYMBOLS[self.list_price.currency.code]

    @property
    def category(self):
        """Return the category instance that this product item belongs"""

        return self.product.category

    @property
    def attributes(self):
        """Return related attribute instances that this product item connect
        with"""

        # Get the related product attribute instances.
        product_attributes = ProductAttribute.objects.filter(
            product_item_attributes_product_attribute__product_item=self
        ).distinct()

        # Get the attribute instances that related to specific product
        # attribute instances.
        attributes = Attribute.objects.filter(
            product_attributes_attribute__in=product_attributes
        )
        return attributes

    @property
    def images(self):
        """Return the ProductItemImage instances that this product item
        related with"""

        return self.product_item_images_product_item.all()

    def clean(self):
        """Restrict the add/change to model fields"""

        if self.is_default:

            if ProductItem.objects.filter(
                    product=self.product,
                    is_default=True
            ).exclude(id=self.id).count() >= 1:
                raise forms.ValidationError(
                    {
                        "is_default": "You can't set more than one default "
                                      "item for the same product"
                    }
                )

    def save(self, *args, **kwargs):
        """On save() method call for this model, update timestamps"""

        # try:
        #     if not self.is_default:
        #         if not ProductItem.objects.filter(
        #             product=self.product,
        #             is_default=True
        #         ).exists():
        #             raise ValueError(
        #                 "You should set at least set one default item for "
        #                 "this product"
        #             )
        # except ValueError as error:
        #     print(str(self), ':', error)
        #
        # else:
        #     return super(
        #         ProductItem,
        #         instance_time_stamp(self)
        #     ).save(*args, **kwargs)
        return super(
            ProductItem,
            instance_time_stamp(self)
        ).save(*args, **kwargs)

    def __str__(self):
        """String representation of model objects"""
        return f'{self.product}, {self.sku}'


class ProductItemImage(TimeStampedModel):
    """Model class to create image instances for product item"""

    # Define model fields.
    # 'slug' set by signal.
    slug = models.SlugField(max_length=100)
    image = ProcessedImageField(
        upload_to=create_image_file_path,
        format='JPEG',
        options={'quality': 100}
    )
    product_item = models.ForeignKey(
        'ProductItem',
        on_delete=models.CASCADE,
        related_name='product_item_images_product_item'
    )

    def save(self, *args, **kwargs):
        """On save() method call for this model, update timestamps"""

        return super(
            ProductItemImage,
            instance_time_stamp(self)
        ).save(*args, **kwargs)

    def __str__(self):
        """String representation of model objects"""
        return f'image/{self.product_item.sku}'


class PromotionItem(models.Model):
    """Model class to set promotion with product item"""

    class Meta:
        """Set metadata for your Model class"""

        constraints = [
            models.UniqueConstraint(
                fields=['promotion', 'product_item'],
                name='promotion_item_unique_appversion'
            )
        ]

    # Define model fields.
    promotion = models.ForeignKey(
        'Promotion',
        on_delete=models.CASCADE,
        related_name='promotion_items_promotion'
    )
    product_item = models.ForeignKey(
        'ProductItem',
        on_delete=models.CASCADE,
        related_name='promotion_items_product_item'
    )

    def __str__(self):
        """String representation of model objects"""
        return f'{self.promotion}, {self.product_item}'


class Attribute(mptt_models.MPTTModel, TimeStampedModel):
    """Model class to create product's attribute instances"""

    # Specify input class field choices, those can be use on frontend to
    # specify value for class attribute.
    INPUT_CLASS_CHOICES = (
        ("option-checkbox", "option-checkbox"),
        ("option-btn", "option-btn"),
        ("option-color", "option-color"),
        ("option-rise-picker", "option-rise-picker")
    )

    class Meta:
        """Set metadata for your Model class"""

        constraints = [
            models.UniqueConstraint(
                fields=['parent', 'title'],
                name='attribute_unique_appversion'
            )
        ]

    # Define model fields.
    # 'slug' set by signal.
    slug = models.SlugField(max_length=100, unique=True)
    thumbnail = ProcessedImageField(
        blank=True,
        upload_to=create_image_file_path,
        format='JPEG',
        options={'quality': 100},
        processors=[ResizeToFit(90, 90)]
    )
    # Note: implement hierarchy of categories using self joining concept.
    # Info: 'TreeOneToOneField', is just a regular 'OneToOneField' that renders
    #       form fields differently in the admin and a few others places.
    # Info: You can’t use a many-to-many as your ‘parent’ field. That’s because
    #       the mptt algorithm only handles trees, not arbitrary graphs. A tree
    #       where nodes can have multiple parents isn’t really a tree at all.
    parent = mptt_models.TreeForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='leaf_nodes'
    )
    title = pg_fields.CICharField(max_length=25, unique=True)
    input_class = models.CharField(
        max_length=20,
        choices=INPUT_CLASS_CHOICES,
        default='check-input'
    )
    display_order = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    def clean(self):
        """Restrict the add/change to model fields"""

        # the fields that defined in class 'mptt' can't be clean if it's not
        # define in your model, it will be None in your model clean() method at
        # add time (Not at change time).

        # if self.display_order is not None:
        #     if Attribute.objects.filter(
        #             parent=self.parent,
        #             display_order=self.display_order
        #     ).exclude(id=self.id).count() >= 1:
        #         raise forms.ValidationError(
        #             {
        #                 'display_order': "You can't set same display order "
        #                                  "to more than one object those in "
        #                                  "the same level of same tree"
        #             }
        #         )
        if self.parent is None:
            if Attribute.objects.filter(title=self.title).exclude(
                    id=self.id).count() >= 1:
                raise forms.ValidationError(
                    {
                        'title': "You already have root node with same "
                                 "category title"
                    }
                )

    def save(self, *args, **kwargs):
        """On save() method call for this model, update timestamps"""

        return super(
            Attribute,
            instance_time_stamp(self)
        ).save(*args, **kwargs)

    def __str__(self):
        """String representation of model objects"""

        full_path = [self.title]
        next_attribute = self.parent
        while next_attribute is not None:
            full_path.append(next_attribute.title)
            next_attribute = next_attribute.parent

        # return the list as string in reverse order.
        # Note: Python sequence slice addresses can be written as
        #       list_name[start:end:step] and any of start, stop or end can be
        #       dropped.
        #       list_name[::3] is every third element of the sequence
        #       (jumping), or can be used to print a list in reverse order.
        return ' / '.join(full_path[::-1])


class CategoryAttribute(models.Model):
    """Model class to create category's attributes"""

    class Meta:
        """Set metadata for your Model class"""

        constraints = [
            models.UniqueConstraint(
                fields=['category', 'attribute'],
                name='category_attribute_unique_appversion'
            )
        ]

    # Define model fields.
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='category_attributes_category'
    )
    attribute = models.ForeignKey(
        'Attribute',
        on_delete=models.CASCADE,
        related_name='category_attributes_attribute'
    )

    def __str__(self):
        """String representation of model objects"""
        return f'{self.category}, {self.attribute}'


class ProductAttribute(models.Model):
    """Model class to set product attributes"""

    # Specify input class field choices, those can be use on frontend to
    # specify value for class attribute.
    # INPUT_CLASS_CHOICES = (
    #     ("option-select", "option-select"),
    #     ("option-btn", "option-btn"),
    #     ("option-color", "option-color"),
    #     ("option-img", "option-img")
    # )

    class Meta:
        """Set metadata for your Model class"""

        # Note: we need to constraint product and attribute fields, so
        #       each product can have specific brand, use_case, ..etc.
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'attribute'],
                name='product_attribute_unique_appversion'
            )
        ]

    # Define model fields.
    # slug = models.SlugField(max_length=100)
    # thumbnail = ProcessedImageField(
    #     blank=True,
    #     upload_to=create_image_file_path,
    #     format='JPEG',
    #     options={'quality': 100}
    # )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='product_attributes_product'
    )
    attribute = models.ForeignKey(
        'Attribute',
        on_delete=models.CASCADE,
        related_name='product_attributes_attribute'
    )
    # input_class = models.CharField(
    #     max_length=20,
    #     choices=INPUT_CLASS_CHOICES,
    #     default='option-select'
    # )
    is_common_attribute = models.BooleanField(
        default=True,
        help_text="By selecting this option as True, means this attribute "
                  "option will not show within the product item attribute "
                  "suggestions for attribute_option field"
    )

    def __str__(self):
        """String representation of model objects"""
        return f'{self.attribute}'


class ProductItemAttribute(models.Model):
    """Model class to set product's item attribute"""

    class Meta:
        """Set metadata for your Model class"""

        # Note: we need to constraint product_item and attribute fields, so
        #       each product item can have specific color, size, style ..etc.
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['product_item', 'product_attribute'],
        #         name='product_item_attribute_unique_appversion'
        #     )
        # ]

    # Define model fields.
    slug = models.SlugField(max_length=100)
    thumbnail = ProcessedImageField(
        blank=True,
        upload_to=create_image_file_path,
        format='JPEG',
        options={'quality': 70},
        processors=[Thumbnail(64, 64)],
    )
    product_item = models.ForeignKey(
        'ProductItem',
        on_delete=models.CASCADE,
        related_name='product_item_attributes_product_item'
    )
    product_attribute = models.ForeignKey(
        'ProductAttribute',
        on_delete=models.CASCADE,
        related_name='product_item_attributes_product_attribute'
    )

    def __str__(self):
        """String representation of model objects"""
        return f'{self.product_attribute}'


class POItem(models.Model):
    """Model class to set product items to a purchase order"""

    class Meta:
        """Set metadata for your Model class"""

        constraints = [
            models.UniqueConstraint(
                fields=['purchase_order', 'product_item'],
                name='po_item_unique_appversion'
            )
        ]

    # Define model fields.
    purchase_order = models.ForeignKey(
        'PurchaseOrder',
        on_delete=models.CASCADE,
        related_name='po_items_purchase_order'
    )
    product_item = models.ForeignKey(
        'ProductItem',
        on_delete=models.PROTECT,
        related_name='po_items_product_item'
    )
    quantity = models.PositiveSmallIntegerField(default=1)
    price_per_unit = MoneyField(
        max_digits=8,
        decimal_places=settings.MONEY_DECIMAL_PLACES,
        default_currency=settings.MONEY_DEFAULT_CURRENCY,
        validators=[
            MinMoneyValidator({'USD': 1}),
            MaxMoneyValidator({'USD': 5000})
        ],
        help_text="You can set the value or automatically will set as "
                  "product item current price"
    )

    @property
    def total_amount(self):
        """Return total amount of price_per_unit multiply by its quantity"""

        if self.price_per_unit:
            return round_money(
                self.price_per_unit.amount * self.quantity,
                self.price_per_unit.currency
            )

    def save(self, *args, **kwargs):
        """On save() method call for this model, we set certain fields value"""

        # In case we didn't specify the price_per_unit, we use the product_item
        # deal_price if available and if not we use the list_price.
        if self.price_per_unit is None:
            self.price_per_unit = self.product_item.deal_price or \
                                  self.product_item.list_price

        return super().save(*args, **kwargs)

    def __str__(self):
        """String representation of model objects"""
        return f'{self.purchase_order}, {self.product_item}'
