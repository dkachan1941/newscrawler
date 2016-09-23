from django.shortcuts import render
from .models import News
import explore
from newscrawler.mod_celery import app as celery_app
from . import tasks
from forms import newsForm
import json
from django.http import HttpResponse

def index(request):
	# explore.stop()
	# tasks.run_lenta_parser()

	# form = newsForm(request.POST)
	# category = request.POST['category']
	# if form.is_valid():
	#     news = form.save(False)
	#     news.category = category
	#     news.save()

	qs = News.objects.all()
	return render(request, 'news/posts.html',{'items': qs,})


def get_news_categories(request):
	if request.is_ajax():
		q = request.GET.get('term', '')
		catgs_list = News.objects.filter(category__icontains = q).values("category").distinct()[:20]
		results = []
		for cat in catgs_list:
			cat_json = {}
			# cat_json['id'] = cat.pk
			cat_json['label'] = cat["category"]
			cat_json['value'] = cat["category"]
			# explore.stop()
			results.append(cat_json)
		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)