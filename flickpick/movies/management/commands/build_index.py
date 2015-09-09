import json
import requests
from decimal import Decimal

from pyelasticsearch import ElasticSearch
from django.core.management.base import BaseCommand

from movies.models import Movie, Director, Actor, Writer, Genre, Person

class Command(BaseCommand):
    """
    Indexes the Movies
    """
    def handle(self, *args, **options):

		es = ElasticSearch('http://localhost:9200/')

		movie_docs = [{
			'id': movie.id, 
			'title': movie.title, 
			'year': movie.year,
			'genres': [{
				'genre': g.name,
			} for g in movie.genres.all()],
			'directors': [{
				'name': d.person.name,
			} for d in movie.directors.all()],
			'actors': [{
				'name': a.person.name,
			} for a in movie.actors.all()],
			'writers': [{
				'name': w.person.name,
			} for w in movie.writers.all()],


		} for movie in Movie.objects.all()]

		try:
			es.bulk((es.index_op(doc, id=doc.pop('id')) for doc in movie_docs), index='movies', doc_type='movie')
			print('successfully indexed {} movies'.format(Movie.objects.count()))
		except Exception, e:
			print(e)