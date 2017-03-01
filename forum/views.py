from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.models import User

from forum.forms import QuestionForm, TopicForm, UserForm
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
@login_required(login_url='login')
def new_question(request, topic_id):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            formToSave = form.save(commit=False)

            formToSave.user = request.user
            formToSave.save()
            return redirect('question_details', pk=topic_id)
    else:
        form = QuestionForm(initial={'question_topic': topic_id})
    return render(request, 'forum/new_question.html', {'form': form})


# Redirects back to topic after question creation
def question_details(request, pk):
    # question = get_object_or_404(Question, pk=pk)
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


class UserFormView(generic.View):
    form_class = UserForm
    template_name = 'forum/registration_form.html'

    # Display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # Prosess form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # cleaned (normalized) data (riktig format)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/forum')
        return render(request, self.template_name, {'form': form})
