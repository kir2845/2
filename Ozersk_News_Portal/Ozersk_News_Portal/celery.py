import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ozersk_News_Portal.settings')

app = Celery('Ozersk_News_Portal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
