from django.db import models
import uuid
import os


def category_image_file_path(instance, filename):
    """Generate file path for a new category image"""

    extension = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{extension}'
    return os.path.join('uploads/categories', filename)


class Category(models.Model):
    """model to categorize the products"""

    class Meta:
        """Customize django default way to plural the class name"""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    # Define model fields.
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(max_length=255, blank=True)
    category_image = models.ImageField(upload_to=category_image_file_path,
                                       blank=True)

    def __str__(self):
        """String representation of model objects"""
        return self.category_name
