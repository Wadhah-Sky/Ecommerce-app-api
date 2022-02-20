"""Tests for your project django admin api"""

from rest_framework import status
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

# Notice:
# 1- Public user is a regular user that not subscribed yet.
# 2- Private user is a subscribed user in the system.
# 3- Superuser is a Private user with extra permissions.

# IMPORTANT: the response for HTTP request from django admin is django
#            'TemplateResponse' and will be text/html object.

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


class AdminSiteTest(TestCase):
    """Tests for django admin page"""

    # The 'setUp' function is a TestCase function that will run before every
    # other tests-functions in the related test class.

    def setUp(self):
        """Set up a sample private user and superuser clients"""

        user_email = 'user@test.com'
        superuser_email = 'superuser@test.com'

        self.client = Client()
        self.user = sample_user(email=user_email)
        self.superuser = sample_superuser(email=superuser_email)

        # Force login of superuser with django authentication.
        self.client.force_login(self.superuser)

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
