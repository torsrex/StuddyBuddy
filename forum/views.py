from django.shortcuts import render
from django.http import HttpResponse
from forum.forms import QuestionForm
from django.shortcuts import redirect


def new_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        question = form.save()
        return redirect('question_details', pk=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'new_question.html', {'form': form})

def question_details(request):
    return render(request, 'question_details.html')

def base(request):
    return render(request, 'base.html')