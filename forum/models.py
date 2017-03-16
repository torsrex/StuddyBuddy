from django.contrib.auth.models import User
from django.db import models
from vote.models import VoteModel


# Create your models here.

class Topic(models.Model):
    topic_name = models.CharField(max_length=60)
    topic_desc = models.CharField(max_length=200)
    topic_created = models.DateTimeField('Date created', auto_now_add=True)  # Automatically stores creation save
    topic_updated = models.DateTimeField('Date updated', auto_now_add=True)  # Automatically updates on save

    def __str__(self):
        return self.topic_name


class Question(VoteModel, models.Model):
    question_name = models.CharField(max_length=60)
    question_text = models.TextField()
    question_created = models.DateTimeField('Date created', auto_now_add=True)  # Automatically stores creation date
    question_updated = models.DateTimeField('Date updated', auto_now=True)  # Automatically updates on save
    question_SuitableForQuiz = models.BooleanField(default=False)  # Stores whether answer can be used for quiz
    question_topic = models.ForeignKey(Topic, related_name='questions')
    user = models.ForeignKey(User, editable=False)

    def __str__(self):
        return self.question_name

    def get_user(self):  # Returns user who created question
        return User.objects.get(pk=self.user_id).username.title()


class Answer(VoteModel, models.Model):
    question = models.ForeignKey(Question, related_name='answers')
    topic = models.ForeignKey(Topic)
    answer_text = models.TextField()
    answer_created = models.DateTimeField('Date created', auto_now_add=True)  # Automatically stores creation save
    answer_updated = models.DateTimeField('Date updated', auto_now_add=True)  # Automatically updates on save
    user = models.ForeignKey(User, editable=False)

    def __str__(self):
        return self.answer_text

    def get_user(self):  # Returns user who created answer
        return User.objects.get(pk=self.user_id).username.title()
