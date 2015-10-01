import os
import urllib

from django.db import models
from django.conf import settings
from django.core.files import File
from django.core.urlresolvers import reverse

from haystack.query import SearchQuerySet


class Tag(models.Model):
	name = models.CharField(max_length=25)

	def __unicode__(self):
		return self.name

class Person(models.Model):
	name = models.CharField(max_length=100)

	def get_absolute_url(self):
		return reverse('person_wrapper', kwargs={'person_id': self.pk})

	def get_api_url(self):
		return reverse('person', kwargs={'person_id': self.pk})

	@property
	def director(self):
		try:
			director = Director.objects.get(person=self)
		except Director.DoesNotExist:
			return False
		return director

	@property
	def actor(self):
		try:
			actor = Actor.objects.get(person=self)
		except Actor.DoesNotExist:
			return False
		return actor

	@property
	def writer(self):
		try:
			writer = Writer.objects.get(person=self)
		except Writer.DoesNotExist:
			return False
		return writer

	def movies(self):
		movies = {}

		if self.director:
			movies['directed'] = [{
				'title': m.title,
				'path': m.get_absolute_url(),
			} for m in self.director.movie_set.all()]

		if self.actor:
			movies['acted'] = [{
				'title': m.title,
				'path': m.get_absolute_url(),
			} for m in self.actor.movie_set.all()]

		if self.writer:
			movies['written'] = [{
				'title': m.title,
				'path': m.get_absolute_url(),
			} for m in self.writer.movie_set.all()]

		return movies

	def __unicode__(self):
		return self.name


class Director(models.Model):
	person = models.ForeignKey(Person)

	def __unicode__(self):
		return self.person.name


class Writer(models.Model):
	WRITER_ROLES = (
        ('novel', 'Novel'),
        ('screenplay', 'Screenplay'),
        ('story', 'Story'),
    )

	person = models.ForeignKey(Person)

	def __unicode__(self):
		return self.person.name


class Actor(models.Model):
	person = models.ForeignKey(Person)

	def __unicode__(self):
		return self.person.name


class Genre(models.Model):
	name = models.CharField(max_length=100)

	def new_releases(self):
		return [{
				'id': m.id,
				'title': m.title,
				'path': m.get_absolute_url(),
				'image': {
                	'url': m.poster_url,
                },
                'year': m.year,
			} for m in self.movie_set.order_by('-year')[:10]]

	def all_movies(self):
		return [{
				'id': m.id,
				'title': m.title,
				'path': m.get_absolute_url(),
				'image': {
                	'url': m.poster_url,
                },
                'year': m.year,
			} for m in self.movie_set.all()]

	def get_api_url(self):
		return reverse('genre', kwargs={'genre_id': self.pk})	

	def get_absolute_url(self):
		return reverse('genre_wrapper', kwargs={'genre_id': self.pk})

	def __unicode__(self):
		return self.name


class Movie(models.Model):
	title = models.CharField(max_length=100, unique=True)
	year = models.CharField(max_length=4)
	released = models.DateField(null=True, blank=True)
	rated = models.CharField(max_length=10, default='N/A')
	plot = models.CharField(max_length=300, null=True, blank=True)
	poster_url = models.URLField(null=True, blank=True)
	
	genres = models.ManyToManyField(Genre)
	directors = models.ManyToManyField(Director)
	writers = models.ManyToManyField(Writer)
	actors = models.ManyToManyField(Actor)
	
	imdb_id = models.CharField(max_length=10)
	notes = models.CharField(max_length=200, null=True, blank=True)

	on_netflix = models.BooleanField(default=False)
	on_amazon = models.BooleanField(default=False)
	on_hulu = models.BooleanField(default=False)

	image = models.ImageField(blank=True)

	tags = models.ManyToManyField(Tag)


	class Meta():
		ordering = ('title', '-year')


	def __unicode__(self):
		return "{0} ({1})".format(self.title, self.year)

	def get_api_url(self):
		return reverse('movie', kwargs={'movie_id': self.pk})

	def get_absolute_url(self):
		return reverse('movie_wrapper', kwargs={'movie_id': self.pk})

	def get_image(self):
		result = urllib.urlretrieve(self.poster_url)

		self.image.save(
			os.path.basename(self.poster_url),
			File(open(result[0]))
		)
		self.save()

	def related(self, max_results=6):
		"""
		Use Haystack to return a list of related movies sorted by
		score, followed by title.
		"""
		more_like_this = SearchQuerySet().more_like_this(self)
		results = []

		for result in more_like_this:
			movie = Movie.objects.get(id=result.pk)
			if result.model_name != Movie._meta.model_name:
				continue
			if self.title and movie.title == movie.title:
				continue

			if self.genres.first() not in movie.genres.all():
				continue

			if max_results is not None and len(results) >= max_results:
				break

			results.append(result)

		related_movies = []
		for m in results:
			movie = Movie.objects.get(pk=m.pk)
			related_movies.append(movie)
		return related_movies
		

