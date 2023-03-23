"""Add any extra configuration to your django backend"""

# This will make sure the 'backend' which created in 'celery.py' is always
# imported when Django starts so that 'shared_task' will use this 'backend'.
from .celery import app as celery_app

__all__ = ('celery_app',)
