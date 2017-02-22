from django import forms
from forum.models import Question, Answer, Topic

class QuestionForm(forms.ModelForm):
    question = forms.CharField(widget=forms.Textarea, help_text = 'Enter your question...', )

    class Meta:
        model = Question
