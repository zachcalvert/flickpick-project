import datetime

from haystack import indexes

from movies.models import Movie, Genre, Director, Actor, Genre


class MovieIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')

    def get_model(self):
        return Movie

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter()