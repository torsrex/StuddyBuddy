from django.views import generic

# Create your views here.

from forum.models import *


class IndexView(generic.ListView):
    template_name = 'forum/index.html'
    context_object_name = 'latest_questions_list'

    def get_queryset(self):
        return Question.objects.order_by('-question_created')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'answer_list': Answer.objects.order_by('-answer_created'),
        })
        return context


class TopicsView(generic.ListView):
    model = Topic
    template_name = 'forum/topics.html'
    context_object_name = 'topics_list'

    def get_queryset(self):
        return Topic.objects.order_by('topic_name')
