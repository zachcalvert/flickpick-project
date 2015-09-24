import datetime

from haystack import indexes

from movies.models import Movie, Genre, Director, Actor, Genre

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
		return super(MovieIndex, self).index_queryset(using).filter(default=False)