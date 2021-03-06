from __future__ import absolute_import

import os

from celery import Celery
from celery.decorators import periodic_task
from celery.task.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newscrawler.settings')

from django.conf import settings

app = Celery('newscrawler')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))