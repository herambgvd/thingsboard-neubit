import os

from celery import Celery
from celery.schedules import crontab  # Import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thingsboard_neubit.settings")

app = Celery("thingsboard_neubit")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Add periodic task with crontab schedule
app.conf.beat_schedule = {
    "thermostat": {
        'task': 'apps.infrastructure.tasks.thermostat_sensor_task',
        'schedule': crontab(minute="*/10"),  # Run every 10 minutes
    }
}
