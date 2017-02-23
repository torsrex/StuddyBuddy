from django import forms
from django.forms import ModelForm
from forum.models import Question, Answer, Topic

class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('question_name', 'question_text',)