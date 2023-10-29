"""Configuration of wait_for_db django helper command"""

# Use django BaseCommand method 'check' with 'databases' argument to validate
# database if it's not fully initialized or not available which could throw
# 'OperationalError' for django.db or psycopg2 in case using Postgres.

from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
import time


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""

        self.stdout.write('Waiting for database...')
        db_up = False

        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
