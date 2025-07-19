import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_security.settings')

app = Celery('backend_security')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
