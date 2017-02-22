from django.views import generic

# Create your views here.

from forum.models import Question, Answer


class IndexView(generic.ListView):
    template_name = 'forum/index.html'
    context_object_name = 'latest_questions_list'

    def get_queryset(self):
        return Question.objects.order_by('-question_created')


class DetailView(generic.ListView):
    model = Question
    template_name = 'forum/detail.html'
    context_object_name = 'detailed_question'


class AnswersView(generic.DetailView):
    model = Answer
    template_name = 'forum/answers.html'
    context_object_name = 'detailed_answer_list'
