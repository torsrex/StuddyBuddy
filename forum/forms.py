from django import forms
from django.contrib.auth.models import User

from forum.models import Question, Topic, Answer
from django.db.models import Q

# from haystack.forms import SearchForm # Haystack Search form import


class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Get 'initial' argument if any
        initial_arguments = kwargs.get('initial', None)
        updated_initial = {}
        if initial_arguments:
            # We have initial arguments, fetch 'user' placeholder variable if any
            question_topic = initial_arguments.get('question_topic', None)
            # Now update the form's initial values if user
            if question_topic:
                updated_initial['question_topic'] = question_topic
        # You can also initialize form fields with hardcoded values
        # or perform complex DB logic here to then perform initialization
        # Finally update the kwargs initial reference
        kwargs.update(initial=updated_initial)
        super(QuestionForm, self).__init__(*args, **kwargs)
        # Update css for form fields
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

        # TODO: Implement quiz if time permits
        # Code for adding css styling to SuitableForQuiz checkbox
        """
        self.fields['question_SuitableForQuiz'].widget.attrs.update({
            'class': 'checkbox'
        })
        """

    class Meta:
        model = Question
        # Fields without SuitableForQuiz checkbox
        fields = ('question_name', 'question_text', 'question_topic')

        # TODO: Implement quiz if time permits
        # fields = ('question_name', 'question_text', 'question_SuitableForQuiz', 'question_topic')


class TopicForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        # Update css for form fields
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Topic
        fields = ('topic_name', 'topic_desc')


class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        # Update css for form fields
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Answer
        fields = ('answer_text', 'question', 'topic')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # Update css for form fields
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

"""
# Haystack custom search form, extends haystack form import
class QuestionSearchForm(SearchForm):
    def no_query_found(self):
        return self.searchqueryset.all()
"""