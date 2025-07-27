from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config", broker='redis://redis:6379/0')

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "task-name": {
        "task": "lms.tasks.send_course_update_email",
        'schedule': crontab(minute='*/1'),
        'args': ('Subject Line', 'Email Message Body', ['example@example.com']),
    },
}
app.conf.timezone = "UTC"
