import os

from celery import Celery
from django.conf import settings

from .settings import CELERY_CONFIG as celery_base_config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

celery_task = Celery(
    celery_base_config['name'],
    namespace=celery_base_config['namespace'],
    broker=celery_base_config['broker'],
    backend=celery_base_config['backend'],
    task_serializer=celery_base_config['task_serializer'],
    result_serializer=celery_base_config['result_serializer'],
    accept_content=celery_base_config['accept_content'],
    broker_connection_retry_on_startup=True,
    celery_task_track_started=True
)


# celery_task.config_from_object(celery_custom_config)
celery_task.config_from_object('django.conf:settings')
celery_task.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
