from celery import Celery
import os

from rpl.settings import CELERY_BROKER_URL

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rpl.settings')

app = Celery('rpl', broker=CELERY_BROKER_URL)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
