from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.views import generic

from forum.forms import QuestionForm
from forum.models import *


class IndexView(generic.ListView):
    template_name = 'forum/index.html'
    context_object_name = 'latest_questions_list'

    def get_queryset(self):
        return Question.objects.order_by('-question_created')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'answer_list': Answer.objects.order_by('answer_created'),
        })
        return context


def new_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        question = form.save()
        return redirect('question_details', pk=question.id)
    else:
        form = QuestionForm()
    return render(request, 'forum/new_question.html', {'form': form})


"""
def question_details(request):
    print("Ting:" +str(request))
    question = QuestionForm.objects.get(pk=id)
    return render(request, 'forum/question_details.html', {'question': question})
"""


def question_details(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'forum/question_details.html', {'question': question})


def base(request):
    return render(request, 'forum/base.html')
