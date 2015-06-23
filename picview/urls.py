__author__ = 'derpson'

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dev_filltags/', views.dev_filltags, name='dev_filltags'),
    url(r'^dev_filllikes/', views.dev_filllikes, name='dev_filllikes'),
    url(r'^$', views.view_pics, name='viewpics'),
]
