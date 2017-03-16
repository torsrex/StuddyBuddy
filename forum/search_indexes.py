import datetime
from haystack import indexes
from forum.models import Question


class QuestionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    question_name = indexes.CharField(model_attr='question_name')
    question_created = indexes.DateTimeField(model_attr='question_created')

    def get_model(self):
        return Question

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(question_created__lte=datetime.datetime.now())
