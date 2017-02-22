from django.conf.urls import url
from django.views.generic import ListView, DetailView
from forum.models import *

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^answers/(?P<question_id>[0-9]+)$', views.AnswersView.as_view(), name='answers'),
]
