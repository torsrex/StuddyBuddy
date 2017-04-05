from collections import Counter
from re import compile
from math import sqrt

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render, redirect
from django.views import generic

from forum.forms import *
from forum.models import *


# Lists questions in accordion view
class IndexView(generic.ListView):
    template_name = 'forum/index.html'
    context_object_name = 'latest_questions_list'

    def get_queryset(self):
        return Question.objects.filter(question_topic_id=self.kwargs["pk"]).order_by(
            '-question_created').prefetch_related(
            'answers').all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'topic_name': Topic.objects.get(pk=self.kwargs["pk"]),  # Fetches topic name for the header
            'form': AnswerForm(initial={'topic': self.kwargs["pk"]})
        })
        return context


# Lists logged in users asked questions
class MyQuestionView(generic.ListView):
    template_name = 'forum/my_question.html'
    context_object_name = 'my_question_list'

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user).order_by(
            '-question_created')  # returns questions asked by logged in user

    def get_context_data(self, **kwargs):
        context = super(MyQuestionView, self).get_context_data(**kwargs)
        context.update({
            'answer_list': Answer.objects.order_by('answer_created'),
            'user_name': self.request.user
        })
        return context


def up_vote(request):
    if request.method == 'POST':
        q = Question.objects.get(pk=request.POST['pk_question'])
        q.votes.up(request.user.id)
    return redirect('/forum/topics/' + request.POST['topic'] + '?cid=' + request.POST['pk_question'])


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


def delete_question_in_index(request):
    if not request.user.has_perm('forum.delete_question'):
        return HttpResponseForbidden('Nope!')
    if request.method == 'POST':
        q = Question.objects.get(pk=request.POST['pk_question'])
        q.delete()
    return redirect('/forum/topics/' + request.POST['topic'])


# Deletes question
def delete_question(request):
    question = get_object_or_404(Question, pk=request.POST['pk_question'])
    question.delete()
    return HttpResponseRedirect('/forum/my_question/')


# Handles the post of new answer form for IndexListView
@login_required(login_url='login')
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
@login_required(login_url='login')
def new_question(request, topic_id):
    if request.method == "POST":
        form = QuestionForm(request.POST)  # Passes arguments in request to form
        if form.is_valid():
            form_to_save = form.save(commit=False)
            form_to_save.user = request.user
            form_to_save.save()
            return redirect('/forum/topics/' + topic_id + '?cid=' ) #TODO:Fix redirect
    else:
        form = QuestionForm(initial={'question_topic': topic_id})  # Creates a new form with initial values
    return render(request, 'forum/new_question.html', {'form': form})  # Returns a render using the form


# Creates new topic
@login_required(login_url='login')
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
