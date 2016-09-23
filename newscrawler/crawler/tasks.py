from __future__ import absolute_import

from celery import shared_task
from django.conf import settings
import urllib2
from lxml import etree
from io import BytesIO
from .models import News
import dateutil.parser
# from . import explore

@shared_task
def run_lenta_parser():
	url = settings.LENTA_RSS_URL
	xml = urllib2.urlopen(url).read()
	tree = etree.parse(BytesIO(xml))
	context = etree.iterparse(BytesIO(xml))
	for action, elem in context:
		if elem.tag == 'item':
			newNews = News.objects.create(title=elem.find('title').text,
                                 text=elem.find('description').text,
                                 date=dateutil.parser.parse(elem.find('pubDate').text),
                                 category=elem.find('category').text)
			newNews.save()