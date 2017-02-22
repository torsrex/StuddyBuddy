from django.conf.urls import url

from forum.views import QuestionListView

urlpatterns = [
    url(r'^$', QuestionListView.as_view(), name='Question-list'),
]