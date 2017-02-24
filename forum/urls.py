from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.TopicsView.as_view(), name='topics'),
    url(r'^topics/(?P<pk>\d+)/$', views.IndexView.as_view(), name='index'),
    url(r'^topics/(?P<topic_id>\d+)/new_question/$', views.new_question, name='new_question'),
    url(r'^new_topic/$', views.new_topic, name='new_topic'),
    url(r'^topics/(?P<pk>\d+)/$', views.question_details, name='question_details'),  # Don't delete this line
]
