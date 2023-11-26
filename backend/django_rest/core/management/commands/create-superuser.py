"""Configuration of create superuser django helper command"""


# from django.contrib.auth.management.commands import createsuperuser
from django.core.management.base import BaseCommand
# from core.management.commands import wait_for_db
import subprocess
import os

# Note: if you want to check which colors is available, check 'termcolors'
#       class.

# Note: In non-interactive mode (using --no-input flag) of Django
#       'createsuperuser' command, the USERNAME_FIELD and required fields
#       (listed in REQUIRED_FIELDS) in the User model, fall back to:
#
#       DJANGO_SUPERUSER_<uppercase_field_name>
#
#       environment variables, unless they are overridden directly by a command
#       line argument.
#       When run interactively, this command will prompt for a password for the
#       new superuser account. When run non-interactively, you can provide
#       a password by setting the 'DJANGO_SUPERUSER_PASSWORD' environment
#       variable. Otherwise, no password will be set, and the superuser account
#       will not be able to log in until a password has been manually set for
#       it.


class Command(BaseCommand):
    """Django command to create superuser in database"""

    # Note: if you have set required values to create superuser as environment
    # variables:

    # DJANGO_SUPERUSER_< uppercase_field_name >

    # And no need to pass these values to the command unless you want to
    # override it.

    def handle(self, *args, **options):
        """Entrypoint for command"""

        self.stdout.write("Creating superuser")

        email = os.getenv('DJANGO_SUPERUSER_EMAIL', '')  # unique
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', '')  # unique
        phone_number = os.getenv('DJANGO_SUPERUSER_PHONE_NUMBER', '')  # unique
        first_name = os.getenv('DJANGO_SUPERUSER_FIRST_NAME', '')
        last_name = os.getenv('DJANGO_SUPERUSER_LAST_NAME', '')

        # Note: here we are using helper command 'wait_for_db'.
        # Remember: password argument will be passed automatically depending on
        #           environment variable 'DJANGO_SUPERUSER_PASSWORD'.
        cmd = f'wait_for_db & ' \
              f'python manage.py createsuperuser ' \
              f'--email={email} ' \
              f'--username="{username}" ' \
              f'--phone_number={phone_number} ' \
              f'--first_name={first_name} ' \
              f'--last_name={last_name} ' \
              f'--no-input'

        result = subprocess.run(
            ["sh", "-c", cmd],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # return system-exit code of the command
        res = str(result.returncode).strip()

        # if exit code isn't 0
        if res != '0':
            self.stdout.write(self.style.ERROR(
                'Error while trying to create superuser, the given info is '
                'already exists!')
            )
