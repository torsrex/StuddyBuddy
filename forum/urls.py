from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^new_question/$', views.new_question, name='new_question'),
    url(r'^question/(?P<pk>\d+)/$', views.question_details, name='question_details'),
    # url(r'^question_details/', views.question_details, name='question_details'),
]
