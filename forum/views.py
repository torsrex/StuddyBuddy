from django.shortcuts import render
from forum.forms import QuestionForm


def add_question(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = QuestionForm(request.POST)

        form.save(commit=True)

        return index(request)

    else:
        form = QuestionForm()

    return render_to_response('forum/add_question.html', {'form': form}, context)
