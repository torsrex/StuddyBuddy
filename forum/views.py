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
            'topic_name': Topic.objects.get(pk=self.kwargs["pk"])  # Fetches topic name for the header
        })
        return context


# Creates new question
def new_question(request, topic_id):
    if request.method == "POST":
        form = QuestionForm(request.POST)  # Passes arguments in request to form
        form.save()
        return redirect('question_details', pk=topic_id)  # Redirects to question_ details view using pk from topic_id
    else:
        form = QuestionForm(initial={'question_topic': topic_id})  # Creates a new form with initial values
    return render(request, 'forum/new_question.html', {'form': form})  # Returns a render using the form


# Redirects back to topic after question creation
def question_details(request, pk):
    return render(request, '/forum/topics/' + pk)


# Creates new topic
def new_topic(request):
    if request.method == "POST":  # Used when submit button is clicked
        form = TopicForm(request.POST)  # Passes arguments in request to form
        form.save()
        return redirect('topics')  # Redirects to the topic view after form submission
    else:
        form = TopicForm()  # Just displays the form empty
    return render(request, 'forum/new_topic.html',
                  {'form': form})  # Returns a render using the template and form specified


# Overview of topics with search function
class TopicsView(generic.ListView):
    model = Topic  # Sets the model this built in view is interacting with
    template_name = 'forum/topics.html'  # Sets template used by the view
    context_object_name = 'topics_list'  # Creates name for list of the object

    def get_queryset(self):
        return Topic.objects.order_by('topic_name')  # Makes sure the topics are ordered by name
