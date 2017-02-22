from django.conf.urls import url

from forum.views import *

urlpatterns = [
    url(r'^add_question/$', add_question, name='add_question'),  # NEW MAPPING!

    url(r'^question/(?P<question_name_url>\w+)$', question, name='question'),
]
