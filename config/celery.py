from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config", broker='redis://localhost:6379/0')

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'task-name': {
        'task': 'myapp.tasks.my_periodic_task',
        'schedule': 10.0,
    },
}
app.conf.timezone = 'UTC'