import datetime

from haystack import indexes

from movies.models import Movie, Person

"""
e.g. http://localhost:9200/movies/_search?q=the
"""

class MovieIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True, 
        template_name="search/indexes/movies/movie_text.txt")
    title = indexes.CharField(model_attr='title')

    def get_model(self):
        return Movie

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return super(MovieIndex, self).index_queryset(using).filter()


class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name="search/indexes/person_text.txt")
    name = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return Person

    def index_queryset(self, using=None):
        return super(PersonIndex, self).index_queryset(using).filter()

