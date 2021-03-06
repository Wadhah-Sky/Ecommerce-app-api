""" Tests for your project models code"""

from unittest.mock import patch
from django.test import TestCase
from django.core.exceptions import ValidationError
from core import models
from django.contrib.auth import get_user_model


# Notice:
# 1- Public user is a regular user that not subscribed yet.
# 2- Private user is a subscribed user in the system.
# 3- Superuser is a Private user with extra permissions.

# Define default user info.
PAYLOAD = {
    'username': 'username test',
    'password': 'test12345678',
    'first_name': 'first',
    'last_name': 'last',
    'phone_number': '+9647722243876'
}


# Define a helper function for creating a user.
def sample_user(**dictionary):
    """Create a private sample user"""

    PAYLOAD.update(dictionary)
    return get_user_model().objects.create_user(**PAYLOAD)


# Define a helper function for creating superuser.
def sample_superuser(**dictionary):
    """Create sample superuser"""

    PAYLOAD.update(dictionary)
    return get_user_model().objects.create_superuser(**PAYLOAD)


class ModelTest(TestCase):
    """Test class for project models"""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""

        # Public user details.
        email = 'test@yahoo.com'
        password = 'test123456'
        user = sample_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""

        # Public user details.
        email = 'test@TEST.COM'

        user = sample_user(email=email)

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test in case creating a new user raises error"""

        # Public user details.
        email = None

        # Check if invalid email value will raise a 'ValueError', otherwise
        # assert an exception.
        with self.assertRaises(ValueError):
            sample_user(email=email)

    def test_create_new_superuser(self):
        """Test creating a new superuser"""

        # Public user details.
        email = 'superuser@test.com'

        superuser = sample_superuser(email=email)

        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_new_user_invalid_phone_number(self):
        """Test that ValidationError exception will raise when enter invalid
        phone number to create a user"""

        email = 'test@test.com'
        invalid_phone_number = '788787'
        PAYLOAD['phone_number'] = invalid_phone_number

        with self.assertRaises(ValidationError):
            sample_user(email=email)

    def test_category_str(self):
        """Test the Category class objects string representation"""

        category = models.Category.objects.create(
            category_name='Test Category',
            slug='www.website.com/test-category',
            description='Text'
        )

        self.assertEqual(str(category), category.category_name)

    @patch('uuid.uuid4')
    def test_category_file_name_uuid(self, mock_uuid4):
        """Test that category image is saved in the correct location"""

        uuid = 'test_uuid'
        mock_uuid4.return_value = uuid

        file_path = models.category_image_file_path(None, 'test.jpg')

        expected_path = f'uploads/categories/{uuid}.jpg'

        self.assertEqual(expected_path, file_path)
