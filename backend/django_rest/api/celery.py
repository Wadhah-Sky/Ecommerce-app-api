"""Configure your project Celery"""

from celery import Celery

from django.conf import settings

import os

# Important: first you have to specify the URL of 'Message Broker' and 'Backend
#            Database' for Celery tasks in your django backend 'settings.py'
#            file.

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

# Define celery instance of the django app by set its name.
app = Celery('api')

# Read config from Django 'settings.py' file.
# Using a string here means the worker doesn't have to serialize the
# configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys should have
# a `CELERY_` prefix in 'settings.py' file.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# Set your Celery tasks class by using decorator to call base.task() function.
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y
