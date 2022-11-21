import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "b3.settings")
app = Celery("b3")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()