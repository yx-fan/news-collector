from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# setup Django settings for 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_news.settings')

# create a Celery application
app = Celery('finance_news')

# load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# discover tasks in all applications
app.autodiscover_tasks()

# configure periodic tasks (Celery Beat configuration)
app.conf.beat_schedule = {
    'fetch-rss-every-hour': {
        'task': 'news.tasks.rss_tasks.fetch_rss_task',
        'schedule': crontab(minute=0, hour='*/1'),  # every hour
    }
}

# run fetch_rss task immediately after starting Celery Beat
from news.tasks.rss_tasks import fetch_rss_task
from celery.signals import worker_ready

@worker_ready.connect
def setup_periodic_tasks(sender, **kwargs):
    print("🚀 Celery started, running fetch_rss immediately...")
    fetch_rss_task.delay()

