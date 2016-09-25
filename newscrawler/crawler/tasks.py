from __future__ import absolute_import

from celery import shared_task
from celery.decorators import task
from django.conf import settings
import urllib2
from lxml import etree
from io import BytesIO
from .models import News
import dateutil.parser as d_parser
# from . import explore
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from xhtml2pdf import pisa as pisa
from cStringIO import StringIO
from django.template import Context, Template
from django.core.mail import EmailMessage
from django.core.mail import get_connection
from django.conf import settings
from django.db.models import Q

@task(name="run_lenta_parser")
@periodic_task(run_every=(crontab(minute='*/3')), name="run_lenta_parser", ignore_result=True)
def run_lenta_parser():
	url = settings.LENTA_RSS_URL
	xml = urllib2.urlopen(url).read()
	tree = etree.parse(BytesIO(xml))
	context = etree.iterparse(BytesIO(xml))
	for action, elem in context:
		if elem.tag == 'item':
			item_exists = News.objects.filter(title=elem.find('title').text)
			if len(item_exists) == 0:
				newNews = News.objects.create(title=elem.find('title').text,
	                                 text=elem.find('description').text,
	                                 date=d_parser.parse(elem.find('pubDate').text),
	                                 category=elem.find('category').text.upper())
				newNews.save()

@task(name="gen_pdf_and_send")
def gen_pdf_and_send(dateFrom, dateTo, category, reciever):
	if category == None:
		qs = News.objects.filter(Q(date__gte=dateFrom), Q(date__lte=dateTo))
	else:
		qs = News.objects.filter(Q(category=category), Q(date__gte=dateFrom), Q(date__lte=dateTo))

	dj_template = """
		<html>
			<head>
			<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
				<style>
					@font-face {
						font-family: Arial;
						src: url(""" + settings.FONT_PATH_ARIAL + """);
					}
					body {
						font-family: Arial;
					}
				</style>  
			</head>
			<body>
				<div>
					{% for post in items %}
					<h3>{{post.title}}</h3>
					<h6>{{post.text}}</h6>
					<h6>{{post.date}}</h6>
					<h6>{{post.category}}</h6>
					<hr>
					{% endfor %}
				</div>
			</body>
		</html>
		"""
	t = Template(dj_template)
	c = Context({'items': qs})
	html = t.render(c)
	pdf = StringIO()
	pisa.CreatePDF(StringIO(html.encode('utf-8')), pdf, encoding='UTF-8')
	connection = get_connection(use_ssl=True, host=settings.EMAIL_HOST, port=settings.EMAIL_PORT,username=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD)
	email = EmailMessage(settings.EMAIL_TITLE, settings.EMAIL_TEXT, settings.EMAIL_HOST_USER, [reciever.encode('utf-8')], connection=connection)
	email.attach('news.pdf', pdf.getvalue(), 'application/pdf')
	email.send()
