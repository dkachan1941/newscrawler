# -*- coding: utf-8 -*-

from django.shortcuts import render
from .models import News
import explore
from newscrawler.mod_celery import app as celery_app
from . import tasks
from forms import newsForm
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from xhtml2pdf import pisa as pisa
from cStringIO import StringIO
from django.template import Context, Template
from django.core.mail import EmailMessage
from django.core.mail import get_connection
from django.conf import settings
from django.db.models import Q
from datetime import datetime

def get_news(request):
	qs = News.objects.all()
	return render(request, 'news/posts.html',{'items': qs,})

@csrf_exempt
def get_filtered_news(request):
	if request.method == 'POST':
		category = request.POST['category'] or None
		dateFrom = datetime(2000, 1, 1) if request.POST['dateFrom'] == "" else request.POST['dateFrom'] + " 00:00:00"
		dateTo = datetime(2100, 1, 1) if request.POST['dateTo'] == "" else request.POST['dateTo'] + " 00:00:00"

		if category == None:
			qs = News.objects.filter(Q(date__gte=dateFrom), Q(date__lte=dateTo))
		else:
			qs = News.objects.filter(Q(category=category), Q(date__gte=dateFrom), Q(date__lte=dateTo))

		jsonNews = {'news': []}
		for post in qs:
			item = {
				'title': post.title,
				'text': post.text,
				'category': post.category,
				'date': post.date.isoformat(),
			}
			jsonNews['news'].append(item)
		result = json.dumps(jsonNews)
		return HttpResponse(result, 'application/javascript')
	else:
		return HttpResponse(str(dict({"error": "Wrong request"})), 'application/javascript')

@csrf_exempt
def send_news_to_email(request):
	if request.method == 'POST':
		category = request.POST['category'] or None
		dateFrom = datetime(2000, 1, 1).isoformat() if request.POST['dateFrom'] == "" else request.POST['dateFrom'] + " 00:00:00"
		dateTo = datetime(2100, 1, 1).isoformat() if request.POST['dateTo'] == "" else request.POST['dateTo'] + " 00:00:00"
		reciever = request.POST['email']

		tasks.gen_pdf_and_send.delay(dateFrom, dateTo, category, reciever)

		return HttpResponse(json.dumps("Задание поставлено в очередь"), 'application/javascript')
	else:
		return HttpResponse(str(dict({"error": "Wrong request"})), 'application/javascript')

def get_categories(request):
	if request.is_ajax():
		q = request.GET.get('term', '').upper()
		catgs_list = News.objects.filter(category__icontains = q).values("category").distinct()[:20]
		results = []
		for cat in catgs_list:
			cat_json = {}
			cat_json['label'] = cat["category"]
			cat_json['value'] = cat["category"]
			results.append(cat_json)
		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)