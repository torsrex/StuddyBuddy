from django.shortcuts import render
from forum.forms import QuestionForm


def new_question(request):
    form_class = QuestionForm

    return render(request, 'new_question.html', {
        'form': form_class,
    })

def base(request):
    return render(request, 'base.html')