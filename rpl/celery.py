from celery import Celery
import os

from rpl.settings import CELERY_BROKER_URL

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rpl.settings')

app = Celery('rpl', broker=CELERY_BROKER_URL) # can remove broker if celery faisl

app.config_from_object('django.conf:settings', namespace='CELERY')

# Force reloading of all tasks
app.tasks.clear()

app.autodiscover_tasks(packages=['submissions'])


# debugging task discovery
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')