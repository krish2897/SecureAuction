import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bidding.settings')

app = Celery('bidding')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'check-auctions-every-minute': {
        'task': 'auction.check_auctions',
        'schedule': crontab(minute='*'),
    },
}