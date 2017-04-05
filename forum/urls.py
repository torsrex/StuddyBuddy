from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^$', views.TopicsView.as_view(), name='topics'),
    url(r'^topics/(?P<pk>\d+)/$', views.IndexView.as_view(), name='index'),
    url(r'^topics/(?P<topic_id>\d+)/new_question/$', views.new_question, name='new_question'),
    url(r'^new_topic/$', views.new_topic, name='new_topic'),
    url(r'^my_question', login_required(views.MyQuestionView.as_view(), login_url='login'), name='my_question'),
    url(r'^new_answer/$', views.new_answer, name='new_answer'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/forum'}, name='logout'),
    url(r'^up_vote/$', views.up_vote, name='up_vote'),
    url(r'^down_vote/$', views.down_vote, name='down_vote'),
    url(r'^up_vote_answer/$', views.up_vote_answer, name='up_vote_answer'),
    url(r'^down_vote_answer/$', views.down_vote_answer, name='down_vote_answer'),
    url(r'^(?P<question_id>[0-9]+)/$', views.delete_question, name="delete_question"),
    url(r'^delete_question_in_index/$', views.delete_question_in_index, name="delete_question_in_index"),
    url(r'^search/$', views.search_for_q, name="search_for_q"),
    url(r'^mark_as_solved/$', views.mark_as_solved, name="mark_as_solved"),
]
