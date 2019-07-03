from django.conf.urls import url,include
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    url(r'^$', views.home, name = 'home'),
    url(r'^check/(?P<uname>.+)$', views.check, name = 'check')

 ]