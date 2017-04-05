from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

# Imports all views
from . import views

urlpatterns = [
    url(r'^$', views.TopicsView.as_view(), name='topics'),
    url(r'^topics/(?P<pk>\d+)/$', views.IndexView.as_view(), name='index'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/forum'}, name='logout'),
    url(r'^topics/(?P<topic_id>\d+)/new_question/$', login_required(views.new_question, login_url='login'),
        name='new_question'),
    url(r'^new_topic/$', login_required(views.new_topic, login_url='login'), name='new_topic'),
    url(r'^my_question', login_required(views.MyQuestionView.as_view(), login_url='login'), name='my_question'),
    url(r'^new_answer/$', login_required(views.new_answer, login_url='login'), name='new_answer'),
    url(r'^up_vote/$', login_required(views.up_vote, login_url='login'), name='up_vote'),
    url(r'^down_vote/$', login_required(views.down_vote, login_url='login'), name='down_vote'),
    url(r'^up_vote_answer/$', login_required(views.up_vote_answer, login_url='login'), name='up_vote_answer'),
    url(r'^down_vote_answer/$', login_required(views.down_vote_answer, login_url='login'), name='down_vote_answer'),
    url(r'^(?P<question_id>[0-9]+)/$', login_required(views.delete_question, login_url='login'),
        name="delete_question"),
    url(r'^delete_question_in_index/$', login_required(views.delete_question_in_index, login_url='login'),
        name="delete_question_in_index"),
    url(r'^search/$', views.search_for_q, name="search_for_q"),
    url(r'^mark_as_solved/$', views.mark_as_solved, name="mark_as_solved"),
]
