
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login
from django.contrib.auth.views import logout

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^news/', include('crawler.urls')),
]
