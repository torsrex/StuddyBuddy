import datetime
from haystack import indexes
from forum.models import Question


# Creates new index for question model, see http://nanvel.name/2013/07/django-haystack-example
class QuestionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)  # Mandatory field in all Index classes
    question_name = indexes.CharField(model_attr='question_name')
    question_text = indexes.CharField(model_attr='question_text')
    question_created = indexes.DateTimeField(model_attr='question_created')

    def get_model(self):
        return Question  # Mandatory method to set model

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(question_created__lte=datetime.datetime.now())  # Returns a queryset
