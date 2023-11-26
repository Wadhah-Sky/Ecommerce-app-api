"""Configuration of wait_for_db django helper command"""

# Use django BaseCommand method 'check' with 'databases' argument to validate
# database if it's not fully initialized or not available which could throw
# 'OperationalError' for django.db or psycopg2 in case using Postgres.

from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
import time

# Info: if you decided to use script entrypoint for django with waiting for
#       database, it's possible to use Netcat 'nz' command:
#
#       while ! nc -z $SQL_HOST $SQL_PORT; do
#          sleep 0.1
#       done
#
#       echo "PostgreSQL started"

# Info: The Netcat ( nc ) command is a command-line utility for reading and
#       writing data between two computer networks. The communication happens
#       using either TCP or UDP.
#       Netcat is useful in scanning ports on a server from your local machine.
#       It is used to know if a specific port is open and/or accepting
#       connections. The -z option is used to just scan for the port but not
#       send any data. It is commonly referred to as zero I/O mode.


class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args, **options):
        """Entrypoint for command"""

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
