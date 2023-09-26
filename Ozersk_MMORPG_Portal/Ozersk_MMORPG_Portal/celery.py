import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ozersk_MMORPG_Portal.settings')

app = Celery('Ozersk_MMORPG_Portal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

