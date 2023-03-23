"""Tests for your project helper commands"""

from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):
    """Tests for your helper commands"""

    @patch('django.core.management.base.BaseCommand.check', return_value=True)
    def test_wait_for_db_ready(self, ck):
        """Test that helper command is working when simulate the behavior of
        django if the database service is available"""

        call_command('wait_for_db')
        self.assertEqual(ck.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for database"""

        with patch('django.core.management.base.BaseCommand.check') as ck:
            ck.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(ck.call_count, 6)
