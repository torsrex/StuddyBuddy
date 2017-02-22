from django import forms
from forum.models import Question, Answer, Topic

class QuestionForm(forms.Form):
    qustion_topic = forms.CharField(required=True)
    question_text = forms.CharField(required=True, widget=forms.Textarea)