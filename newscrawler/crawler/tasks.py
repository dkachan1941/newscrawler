from __future__ import absolute_import

from celery import shared_task
from django.conf import settings
import lxml.html as lh
import urllib2
from . import explore

@shared_task
def run_lenta_parser():
    url = settings.LENTA_RSS_URL
    explore.stop()
    doc=lh.parse(urllib2.urlopen(url))

