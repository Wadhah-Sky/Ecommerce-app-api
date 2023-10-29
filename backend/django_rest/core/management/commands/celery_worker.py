"""Configuration of celery_worker command to restart the Celery workers every
 time you make code changes to a task"""

import shlex
import sys
import subprocess

from django.core.management.base import BaseCommand
from django.utils import autoreload


def restart_celery():
    cmd = 'pkill -f "celery worker"'
    if sys.platform == 'win32':
        cmd = 'taskkill /f /t /im celery.exe'

    # call the cmd command of kill process to celery worker.
    # Note: shlex.split method will create list of strings that can be executed
    #       by call() method, it's useful for long command that consists of
    #       multiple sub-commands and arguments.
    #       Info: it's not working with subprocess run() method.
    subprocess.call(shlex.split(cmd))
    # call command to start celery worker.
    subprocess.call(
        shlex.split('celery -A api worker --loglevel=info')
    )


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Starting celery worker with autoreload...')
        autoreload.run_with_reloader(restart_celery)
