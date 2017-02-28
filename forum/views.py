from django.shortcuts import render, redirect
from django.views import generic

from forum.forms import QuestionForm, TopicForm
from forum.models import *


# Lists questions in accordion view
class IndexView(generic.ListView):
    template_name = 'forum/index.html'
    context_object_name = 'latest_questions_list'

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Question.objects.filter(question_topic_id=pk).order_by('-question_created')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'answer_list': Answer.objects.order_by('answer_created'),
        })
        return context


# Creates new question
def new_question(request, topic_id):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        form.save()
        return redirect('question_details', pk=topic_id)
    else:
        form = QuestionForm(initial={'question_topic': topic_id})
    return render(request, 'forum/new_question.html', {'form': form})


# Redirects back to topic after question creation
def question_details(request, pk):
    return render(request, '/forum/topics/' + pk)


# Creates new topic
def new_topic(request):
    if request.method == "POST":
        form = TopicForm(request.POST)
        form.save()
        return redirect('topics')
    else:
        form = TopicForm()
    return render(request, 'forum/new_topic.html', {'form': form})


# Overview of topics with search funcion
class TopicsView(generic.ListView):
    model = Topic
    template_name = 'forum/topics.html'
    context_object_name = 'topics_list'

    def get_queryset(self):
        return Topic.objects.order_by('topic_name')
