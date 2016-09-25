
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.get_news, name='get_news'),
    url(r'^get_categories', views.get_categories, name='get_categories'),
    url(r'^get_filtered_news', views.get_filtered_news, name='get_filtered_news'),
    url(r'^send_news_to_email', views.send_news_to_email, name='send_news_to_email'),
]
