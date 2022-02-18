""" Tests for your project models.py code"""

from unittest.mock import patch
from django.test import TestCase
from core import models


class ModelTest(TestCase):
    """Test class for project models"""

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
