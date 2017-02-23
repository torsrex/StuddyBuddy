from django.conf.urls import url
from django.views.generic import ListView, DetailView
from forum.models import *

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^topics/$', views.TopicsView.as_view(), name='topics'),
    #url(r'^topics/$', views.IndexView.as_view(), name='questionList'),
]
