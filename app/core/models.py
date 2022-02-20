from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.validators import validate_international_phonenumber
from django.contrib.auth.models import AbstractBaseUser, \
                                       PermissionsMixin, \
                                       BaseUserManager
from django.utils import timezone
import uuid
import os


def category_image_file_path(instance, filename):
    """Generate file path for a new category image"""

    extension = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{extension}'
    return os.path.join('uploads/categories', filename)


class UserManager(BaseUserManager):
    """User model manager"""

    def create_user(self, email, username, password=None, **extra_fields):
        """Creates and save new use"""

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

        # Add extra permissions.
        user.is_superuser = True
        user.is_staff = True

        # update user object in database with the extra permissions.
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""

    # Define model fields.
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    phone_number = PhoneNumberField(unique=True, blank=True, null=False)
    date_joined = models.DateTimeField()
    date_modified = models.DateTimeField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Hook in the custom model manager.
    objects = UserManager()

    # Change default username field of user model to be the email field.
    USERNAME_FIELD = 'email'

    # Specify required fields for register a new user.
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def save(self, *args, **kwargs):
        """On save() method call for this model, update timestamps"""

        # Use this way to set time of user joining or profile modified rather
        # than using 'auto_now_add' or 'auto_now' argument because it will set
        # the related field to have 'editable=True' which means this field will
        # not show on admin page by default, you can set it later to be
        # 'read_only' by customizing the admin site for this model.

        # If object who using save() method don't have an 'id' yet, this means
        # he is a new user object.
        if not self.id:
            self.date_joined = timezone.now()

        self.date_modified = timezone.now()
        return super(User, self).save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        """Returns True if the user has the specified permission"""

        # Where 'perm' is in the format "<app label>.<permission codename>"
        # If 'obj' is passed in, this method won’t check for a permission for
        # the model, but for this specific object.
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Returns True if the user has any permissions in the given package
        (the Django app label)"""

        return True

    def full_name(self):
        """Return full name of user by using his first and last name"""

        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        """String representation of model objects"""

        return self.email


class Category(models.Model):
    """model to categorize the products"""

    class Meta:
        """Customize django default way to plural the class name"""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    # Define model fields.
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    category_image = models.ImageField(upload_to=category_image_file_path,
                                       blank=True)

    def __str__(self):
        """String representation of model objects"""
        return self.category_name
