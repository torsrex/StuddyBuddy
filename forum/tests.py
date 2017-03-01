from django.test import TestCase
from django.test import Client
from django.urls import reverse
from forum.models import Question
from forum.forms import QuestionForm
#from django.db import models
#from models.py import Question

# Create your tests here.

class siteTestCase(TestCase):
    def root_page_404(self):
        client = Client()
        response=client.get('/') #forventer 404
        self.assertEquals(response.status_code,404)

    def forum_exists(self):
        client = Client()
        response=client.get('/forum/') #forventer 200
        self.assertEquals(response.status_code,200)

    def new_question_exists(self):
        client = Client()
        response=client.get('/forum/topics/0/new_question/') #forventer 200
        self.assertEquals(response.status_code,200)


class QuestionTestCase(TestCase):
    def question_not_suitable_for_quiz(self):
        r=Question()
        r.question_name="hei"
        self.assertEquals(r.question_SuitableForQuiz,False)

