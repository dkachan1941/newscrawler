
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get_news_categories/', views.get_news_categories, name='get_news_categories'),

    # url(r'^post_detail/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    # url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
]
