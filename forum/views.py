from django.shortcuts import render
from django.views.generic.list import ListView

# Create your views here.

from forum.models import Question


class QuestionListView(ListView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super(QuestionListView, self, ).get_context_data(**kwargs)
        return context
