# Necessary imports for search method
from collections import Counter
from math import sqrt
from re import compile

# Imports used for authenticating
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Permission
# Rendering and view related imports
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render, redirect
from django.views import generic

# Importing forms and models
from forum.forms import *
from forum.models import *


# Overview of topics
class TopicsView(generic.ListView):
    template_name = 'forum/index_topics.html'  # Sets template used by the view
    context_object_name = 'topics_list'  # Creates name for list of the object

    def get_queryset(self):
        return Topic.objects.order_by('topic_name')  # Returns topic queryset ordered by name


# Generic view to lists all questions under topics
class IndexView(generic.ListView):
    template_name = 'forum/question_list.html'
    context_object_name = 'latest_questions_list'  # Sets context variable name (list) used for listing questions

    def get_queryset(self):
        # One-liner, uses topic id to get related questions, orders by question created and fetches related answers
        return Question.objects.filter(question_topic_id=self.kwargs["pk"]).order_by(
            'question_solved', '-vote_score', '-question_created').prefetch_related(
            'answers').all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)  # Adds latest_questions_list context data
        context.update({
            'topic_name': Topic.objects.get(pk=self.kwargs["pk"]),  # Fetches topic name for the header
            'form': AnswerForm(initial={'topic': self.kwargs["pk"]})  # Creates answer form with initial topic value
        })
        return context


# Creates new answer
def new_answer(request):
    if request.method == "POST":  # Used when submit button is clicked
        form = AnswerForm(request.POST)  # Passes arguments in request to form
        if form.is_valid():
            form_to_save = form.save(commit=False)
            form_to_save.user = request.user
            form_to_save.save()
            return redirect(
                '/forum/topics/' + request.POST['topic'] + '?cid=' + request.POST[
                    'question'])  # Redirects to the topic view after form submission


# Creates new question
def new_question(request, topic_id):
    if request.method == "POST":
        form = QuestionForm(request.POST)  # Passes arguments in request to form
        if form.is_valid():
            form_to_save = form.save(commit=False)
            form_to_save.user = request.user
            form_to_save.save()
            return redirect(
                '/forum/topics/' + topic_id + '?cid=' + str(form_to_save.id))  # Redirects to newly created question
    else:
        form = QuestionForm(initial={'question_topic': topic_id})  # Creates a new form with initial values
    return render(request, 'forum/new_question.html', {'form': form})  # Returns a render using the form


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


# Method for handling mark questions as solved
def mark_as_solved(request):
    q = Question.objects.get(pk=request.POST['pk_question'])  # Gets the question
    if q.question_solved is False:  # Checks if question is already solved
        q.question_solved = True  # Marks as solved
        q.save()  # Saves updated question
    else:
        q.question_solved = False  # Marks as unsolved
        q.save()
    return redirect(
        '/forum/topics/' + request.POST['topic'] + '?cid=' + request.POST['pk_question'])  # Redirects to question


# Lists logged in user's asked questions
class MyQuestionView(generic.ListView):
    template_name = 'forum/my_question.html'  # Sets template
    context_object_name = 'my_question_list'  # Sets context variable name

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user).order_by(
            '-question_created')  # returns questions asked by logged in user ordered by creation date


# Method to handle deletion of question in question list under topics (IndexView)
def delete_question_in_index(request):
    if not request.user.has_perm('forum.delete_question'):
        return HttpResponseForbidden()  # Checks if user has permission to delete question
    if request.method == 'POST':
        q = Question.objects.get(pk=request.POST['pk_question'])  # Gets question to be deleted
        q.delete()
    return redirect('/forum/topics/' + request.POST['topic'])  # Redirects back to question list


# Deletes question in my question_list
def delete_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)  # Gets question or returns 404 if not found
    if request.user != question.get_user():
        return HttpResponseForbidden()
    question.delete()
    return HttpResponseRedirect('/forum/my_question/')  # Redirects back to my question list


class UserFormView(generic.View):
    form_class = UserForm  # Sets this class' form to user form
    template_name = 'registration/registration_form.html'

    # Display blank form initially
    def get(self, request):
        form = self.form_class(None)  # Assigns empty form to form variable
        return render(request, self.template_name, {'form': form})  # returns a render with empty form

    # Process form data
    def post(self, request):
        form = self.form_class(request.POST)  # Fills in form with POST data

        if form.is_valid():
            user = form.save(commit=False)  # Saves form temporarily in user variable

            # cleaned (normalized) data (correct format)

            username = form.cleaned_data['username']  # Gets cleaned version of username
            password = form.cleaned_data['password']  # Gets cleaned version of password
            email = form.cleaned_data['email']  # Gets cleaned version of email
            user.set_password(password)  # Adds user password
            user.save()
            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)

            # Sets permissions
            if '@ntnu.no' in email:
                permission = Permission.objects.get(codename='delete_question')
                user.user_permissions.add(permission)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/forum')
        return render(request, self.template_name, {'form': form})


def search_for_q(request):
    q = request.GET['q']
    word = compile(r'\w+')
    top3 = {0: None, 0.0001: None, 0.0000001: None}
    vec1 = Counter(word.findall(q))
    for que in Question.objects.values():
        vec2 = Counter(word.findall(que.get('question_text')))

        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
        sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
        denominator = sqrt(sum1) * sqrt(sum2)

        if not denominator:
            r = 0.0
        else:
            r = float(numerator) / denominator

        minimum = 1
        for my_key, my_value in top3.items():  # iterates through top 3 dict
            if my_key < minimum:
                minimum = my_key

        if r > minimum:
            top3.pop(minimum)
            top3[r] = que

    result = []
    for my_key, my_value in top3.items():
        if top3.get(my_key) is not None:
            result.append(top3.get(my_key))
    return render(request, 'forum/search_result.html', {'result': result})


def up_vote(request):
    if request.method == 'POST':
        q = Question.objects.get(pk=request.POST['pk_question'])  # Fetches question
        q.votes.up(request.user.id)  # Up votes question and stores user id
    return redirect(
        '/forum/topics/' + request.POST['topic'] + '?cid=' + request.POST[
            'pk_question'])  # Redirects to changed question


def down_vote(request):
    if request.method == 'POST':
        q = Question.objects.get(pk=request.POST['pk_question'])
        q.votes.down(request.user.id)
    return redirect('/forum/topics/' + request.POST['topic'] + '?cid=' + request.POST['pk_question'])


def up_vote_answer(request):
    if request.method == 'POST':
        a = Answer.objects.get(pk=request.POST['pk_answer'])
        a.votes.up(request.user.id)
    return redirect('/forum/topics/' + request.POST['topic'] + '?cid=' + request.POST['pk_question'])


def down_vote_answer(request):
    if request.method == 'POST':
        a = Answer.objects.get(pk=request.POST['pk_answer'])
        a.votes.down(request.user.id)
    return redirect('/forum/topics/' + request.POST['topic'] + '?cid=' + request.POST['pk_question'])
