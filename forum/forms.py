from django import forms

from forum.models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_name', 'question_text', 'question_topic', 'question_SuitableForQuiz')
