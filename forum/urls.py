from django.conf.urls import url
from . import views
from forum.views import *

urlpatterns = [
    url(r'^$', views.base, name='home'),
    url(r'^new_question/$', views.new_question, name='new_question'),
    url(r'^question_details/$', views.question_details, name='question_details'),
]
