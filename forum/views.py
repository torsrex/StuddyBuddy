from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render, redirect, render_to_response
from django.views import generic
from haystack.forms import SearchForm

from forum.forms import *
from forum.models import *


# Lists questions in accordion view
class IndexView(generic.ListView):
    template_name = 'forum/index.html'
    context_object_name = 'latest_questions_list'

    def get_queryset(self):
        self.pk = self.kwargs["pk"]
        self.form = AnswerForm(initial={'topic': self.pk})
        return Question.objects.filter(question_topic_id=self.pk).order_by('-vote_score')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'answer_list': Answer.objects.filter(topic=self.pk).order_by('answer_created'),
            'topic_name': Topic.objects.get(pk=self.kwargs["pk"]),  # Fetches topic name for the header
            'form': self.form
        })
        return context


# Lists inlogged users asked questions
class my_questionView(generic.ListView):
    template_name = 'forum/my_question.html'
    context_object_name = 'my_question_list'

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user).order_by(
            '-question_created')  # returns questions asked by inlogged user

    def get_context_data(self, **kwargs):
        context = super(my_questionView, self).get_context_data(**kwargs)
        context.update({
            'answer_list': Answer.objects.order_by('answer_created'),
            'user_name': self.request.user
        })
        return context


def upvote(request):
    if request.method == 'POST':
        q = Question.objects.get(pk=request.POST['pk_question'])
        q.votes.up(request.user.id)
    return redirect('/forum/topics/' + request.POST['topic'] + '?cid=' + request.POST['pk_question'])


def downvote(request):
    if request.method == 'POST':
        q = Question.objects.get(pk=request.POST['pk_question'])
        q.votes.down(request.user.id)
    return redirect('/forum/topics/' + request.POST['topic'] + '?cid=' + request.POST['pk_question'])

def upvote_answer(request):
    if request.method == 'POST':
        a = Answer.objects.get(pk=request.POST['pk_answer'])
        a.votes.up(request.user.id)
    return redirect('/forum/topics/' + request.POST['topic'] + '?cid=' + request.POST['pk_question'])

def downvote_answer(request):
    if request.method == 'POST':
        a = Answer.objects.get(pk=request.POST['pk_answer'])
        a.votes.down(request.user.id)
    return redirect('/forum/topics/' + request.POST['topic'] + '?cid=' + request.POST['pk_question'])

def delete_question_in_index(request):
    if not request.user.has_perm('forum.delete_question'):
        return HttpResponseForbidden('Nope!')
    if request.method == 'POST':
        q = Question.objects.get(pk=request.POST['pk_question'])
        q.delete()
    return redirect('/forum/topics/' + request.POST['topic'])


# Handles the post of new answer form for IndexListView
@login_required(login_url='login')
def new_answer(request):
    if request.method == "POST":  # Used when submit button is clicked
        form = AnswerForm(request.POST)  # Passes arguments in request to form
        if form.is_valid():
            formToSave = form.save(commit=False)
            formToSave.user = request.user
            formToSave.save()
            return redirect(
                '/forum/topics/' + request.POST['topic'])  # Redirects to the topic view after form submission


# Creates new question
@login_required(login_url='login')
def new_question(request, topic_id):
    if request.method == "POST":
        form = QuestionForm(request.POST)  # Passes arguments in request to form
        if form.is_valid():
            formToSave = form.save(commit=False)

            formToSave.user = request.user
            formToSave.save()
            return redirect('question_details', pk=topic_id)
    else:
        form = QuestionForm(initial={'question_topic': topic_id})  # Creates a new form with initial values
    return render(request, 'forum/new_question.html', {'form': form})  # Returns a render using the form


# Deletes question
def delete_question(request, question_id):
    id = question_id
    question = get_object_or_404(Question, pk=id)
    question.delete()
    return HttpResponseRedirect('/forum/my_question/')


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


class UserFormView(generic.View):
    form_class = UserForm
    template_name = 'registration/registration_form.html'

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
            email = form.cleaned_data['email']
            user.set_password(password)
            user.save()
            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)
            if '@ntnu.no' in email:
                permission = Permission.objects.get(codename='delete_question')
                user.user_permissions.add(permission)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/forum')
        return render(request, self.template_name, {'form': form})


# Haystack handle search

def questions(request):
    form = SearchForm(request.GET)
    questions = form.search()  # Returns all results from search
    return render_to_response('forum/questions.html', {'questions': questions})


