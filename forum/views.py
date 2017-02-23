from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from forum.forms import QuestionForm
from django.shortcuts import redirect
from forum.models import *


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