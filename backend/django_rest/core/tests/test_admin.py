"""Tests for your project django admin api"""

import tempfile
import os
from rest_framework import status
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from PIL import Image
from core import models

# Notice:
# 1- Public user is a regular user that not subscribed yet.
# 2- Private user is a subscribed user in the system.
# 3- Superuser is a Private user with extra permissions.

# IMPORTANT: the response for HTTP request from django admin is django
#            'TemplateResponse' and will be text/html object.

# NOTE: each admin url consists of the following three things
#       <the backend name_the name of the model_the name of the admin view>


# Define default user info.
USER_PAYLOAD = {
    'username': 'user test',
    'password': 'test12345611',
    'first_name': 'first',
    'last_name': 'last',
    'phone_number': '+9647722243876'
}

# Define default superuser info.
SUPERUSER_PAYLOAD = {
    'username': 'superuser test',
    'password': 'test12345611',
    'first_name': 'super',
    'last_name': 'user',
    'phone_number': '+9647733343876'
}


# Define a helper function for creating a user.
def sample_user(**dictionary):
    """Create a private sample user"""

    USER_PAYLOAD.update(dictionary)
    return get_user_model().objects.create_user(**USER_PAYLOAD)


# Define a helper function for creating superuser.
def sample_superuser(**dictionary):
    """Create sample superuser"""

    SUPERUSER_PAYLOAD.update(dictionary)
    return get_user_model().objects.create_superuser(**SUPERUSER_PAYLOAD)


# Define a helper function for creating category.
def sample_category(**dictionary):
    """Create sample category"""

    return models.Category.objects.create(**dictionary)


# Define a helper function for creating product.
def sample_product(**dictionary):
    """Create sample product"""

    return models.Product.objects.create(**dictionary)


class AdminSiteTest(TestCase):
    """Tests for django admin page"""

    # The 'setUp' function is a TestCase function that will run before every
    # other tests-functions in the related test class.

    def setUp(self):
        """Set up a samples clients and models objects"""

        user_email = 'user@test.com'
        superuser_email = 'superuser@test.com'

        self.client = APIClient()
        self.user = sample_user(email=user_email)
        self.superuser = sample_superuser(email=superuser_email)

        # Force login of superuser with django authentication.
        self.client.force_login(self.superuser)

        # Define a sample category object.
        self.category = sample_category(title='Jeans')

        # Define a sample product object with info for not-null fields.
        self.product = sample_product(title='AXC Jeans',
                                      category=self.category)

    def test_users_listed(self):
        """"Test that users are listed on the django admin users page"""

        url = reverse('admin:core_user_changelist')

        http_response = self.client.get(url)

        self.assertContains(http_response, self.user.email)
        self.assertContains(http_response, self.superuser.email)

    def test_user_change_page(self):
        """Test that the django admin user edit page works correctly"""

        url = reverse('admin:core_user_change', args=[self.user.id])

        http_response = self.client.get(url)

        self.assertEqual(http_response.status_code, status.HTTP_200_OK)

    def test_add_user_page(self):
        """Test that the add page of a new user works properly"""

        url = reverse('admin:core_user_add')

        http_response = self.client.get(url)

        self.assertEqual(http_response.status_code, status.HTTP_200_OK)

    def test_categories_listed(self):
        """"Test that categories are listed on the django admin categories
         page"""

        url = reverse('admin:core_category_changelist')

        http_response = self.client.get(url)

        self.assertContains(http_response, self.category.title)

    def test_category_change_page(self):
        """Test that the django admin category edit page works correctly"""

        url = reverse('admin:core_category_change', args=[self.category.id])

        http_response = self.client.get(url)

        self.assertEqual(http_response.status_code, status.HTTP_200_OK)

    def test_add_category_page(self):
        """Test that the add page of a new category works properly"""

        url = reverse('admin:core_category_add')

        http_response = self.client.get(url)

        self.assertEqual(http_response.status_code, status.HTTP_200_OK)

    def test_products_listed(self):
        """"Test that products are listed on the django admin products
         page"""

        url = reverse('admin:core_product_changelist')

        http_response = self.client.get(url)

        self.assertContains(http_response, self.product.title)

    def test_product_change_page(self):
        """Test that the django admin product edit page works correctly"""

        url = reverse('admin:core_product_change', args=[self.product.id])

        http_response = self.client.get(url)

        self.assertEqual(http_response.status_code, status.HTTP_200_OK)

    def test_add_product_page(self):
        """Test that the add page of a new product works properly"""

        url = reverse('admin:core_product_add')

        http_response = self.client.get(url)

        self.assertEqual(http_response.status_code, status.HTTP_200_OK)


class AdminSiteUploadFileTest(TestCase):
    """Test class for uploading files to django admin web page"""

    def setUp(self):
        """Set up samples objects"""

        superuser_email = 'superuser@test.com'

        self.client = APIClient()

        self.superuser = sample_superuser(email=superuser_email)

        # Force login of superuser with django authentication.
        self.client.force_login(self.superuser)

    # The 'tearDown' function is a TestCase function that will run after each
    # test function of this class is done, to clean the file system and
    # restore initial state of setUp() function.

    def tearDown(self):
        """Clean file system and restore initial setup state after each test"""

    def test_add_category_with_image(self):
        """Test create category object with image"""

        url = reverse('admin:core_category_add')

        # Create temporary file with '.jpg' extension.
        with tempfile.NamedTemporaryFile(suffix='.jpg') as named_temp_file:

            # Create colored image object with size of tuple 10x10 pixels.
            image_object = Image.new('RGB', (10, 10))

            # Write the image object to named temporary file as JPEG format.
            image_object.save(named_temp_file, format='JPEG')

            # Reset the pointer of seek to the beginning of the file.
            named_temp_file.seek(0)

            # Make HTTP post request.
            http_response = self.client.post(
                url,
                {
                    'title': 'Hat',
                    'slug': 'hat',
                    'thumbnail': named_temp_file
                }
            )

        # Retrieve queryset of database table objects.
        obj = models.Category.objects.all()

        # Confirm that the returned value of 'path' property function for
        # 'thumbnail' attribute value is found in the system path.
        self.assertTrue(os.path.exists(obj[0].thumbnail.path))

        # Check that the http_response status code is 302,
        # which means url will redirect to '/admin/core/category/'.
        self.assertEqual(http_response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(http_response.url, '/admin/core/category/')

    def test_add_category_with_image_bad_request(self):
        """Test uploading an invalid image to new category object"""

        # Note: 'change' page of django admin using HTTP POST method not PATCH
        # or PUT.

        url = reverse('admin:core_category_add')

        # Using context manager create temporary file with '.txt' extension and
        # able to write + read.
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt') as ntp:
            ntp.write('Hello!')
            ntp.seek(0)

            # Make HTTP post request.
            http_response = self.client.post(
                url,
                {
                    'title': 'Hat',
                    'slug': 'hat',
                    'thumbnail': ntp
                }
            )

        # Confirm that admin 'add' site will not re-directed '302'.
        self.assertNotEqual(http_response.status_code, status.HTTP_302_FOUND)

        # Retrieve queryset of database table objects.
        obj = models.Category.objects.all()

        # Confirm that no objects added to the database table.
        self.assertEqual(obj.count(), 0)

    def test_upload_image_to_category(self):
        """Test upload an image to existed category object"""

        # Note: 'change' page of django admin using HTTP POST method not PATCH
        # or PUT.

        category = sample_category(title='Jeans', slug='jeans')

        url = reverse('admin:core_category_change', args=[category.id])

        # Create temporary file with '.jpg' extension.
        with tempfile.NamedTemporaryFile(suffix='.jpg') as named_temp_file:
            # Create colored image object with size of tuple 10x10 pixels.
            image_object = Image.new('RGB', (10, 10))

            # Write the image object to named temporary file as JPEG format.
            image_object.save(named_temp_file, format='JPEG')

            # Reset the pointer of seek to the beginning of the file.
            named_temp_file.seek(0)

            # Make HTTP post request.
            http_response = self.client.post(
                url,
                {
                    'title': 'Jeans',
                    'slug': 'jeans',
                    'thumbnail': named_temp_file
                }
            )

        # Check that the http_response status code is 302.
        self.assertEqual(http_response.status_code, status.HTTP_302_FOUND)

        # Refresh the data of category object.
        category.refresh_from_db()

        # Retrieve queryset of database table objects.
        obj = models.Category.objects.all()

        # Confirm that the returned value of 'path' property function for
        # 'thumbnail' attribute value is found in the system path.
        self.assertTrue(os.path.exists(category.thumbnail.path))

        # Check that the count of list items (dictionaries) for the retrieved
        # queryset object is one.
        self.assertEqual(obj.count(), 1)

        # Confirm that the id of retrieved object from database is the same
        # that we created before.
        self.assertEqual(obj[0].id, category.id)

    def test_upload_image_to_category_bad_request(self):
        """Test uploading an invalid image"""

        # Note: 'change' page of django admin using HTTP POST method not PATCH
        # or PUT.

        category = sample_category(title='Jackets', slug='jackets')

        url = reverse('admin:core_category_change', args=[category.id])

        # Using context manager create temporary file with '.txt' extension and
        # able to write + read.
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt') as ntp:
            ntp.write('Hello!')
            ntp.seek(0)

            # Make HTTP post request.
            http_response = self.client.post(
                url,
                {
                    'title': 'Jeans',
                    'slug': 'jeans',
                    'thumbnail': ntp
                }
            )

        # Confirm that admin 'change' site will not re-directed '302'.
        self.assertNotEqual(http_response.status_code, status.HTTP_302_FOUND)
