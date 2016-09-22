from django.shortcuts import render
from .models import News
import explore
from newscrawler.mod_celery import app as celery_app
from . import tasks

def index(request):
	# explore.stop()
	tasks.run_lenta_parser()
	qs = News.objects.all()
	return render(request, 'news/posts.html',{'items': qs})