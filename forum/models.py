from django.db import models


# Create your models here.

class Topic(models.Model):
    topic_name = models.CharField(max_length=60)
    topic_desc = models.CharField(max_length=200)
    topic_created = models.DateTimeField('Date created', auto_now_add=True)  # Automatically stores creation save
    topic_updated = models.DateTimeField('Date updated', auto_now_add=True)  # Automatically updates on save


class Question(models.Model):
    question_name = models.CharField(max_length=60)
    question_text = models.TextField()
    question_created = models.DateTimeField('Date created', auto_now_add=True)  # Automatically stores creation date
    question_updated = models.DateTimeField('Date updated', auto_now=True)  # Automatically updates on save
    question_SuitableForQuiz = models.BooleanField(default=False)  # Stores whether answer can be used for quiz
    #question_topic = models.ForeignKey(Topic, related_name='questions')


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers')
    topic = models.ForeignKey(Topic)
    answer_text = models.TextField()
    answer_created = models.DateTimeField('Date created', auto_now_add=True)  # Automatically stores creation save
    answer_updated = models.DateTimeField('Date updated', auto_now_add=True)  # Automatically updates on save
