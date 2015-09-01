from django.db import models

from django.core.urlresolvers import reverse

class Genre(models.Model):
	name = models.CharField(max_length=100)

	def get_absolute_url(self):
		return reverse('genre_browse', kwargs={'genre_id': self.pk})

	def __unicode__(self):
		return self.name

class Director(models.Model):
	name = models.CharField(max_length=100)

	@property
	def movies(self):
		return Movie.objects.filter(director=self)

	def __unicode__(self):
		return self.name

class Writer(models.Model):
	name = models.CharField(max_length=100)

	@property
	def movies(self):
		return Movie.objects.filter(writers__contains=self)

	def __unicode__(self):
		return self.name

class Actor(models.Model):
	name = models.CharField(max_length=100)

	@property
	def movies(self):
		return Movie.objects.filter(actors__contains=self)

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
	imdb_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
	notes = models.CharField(max_length=200, null=True, blank=True)

	on_netflix = models.BooleanField(default=False)
	on_amazon = models.BooleanField(default=False)
	on_hulu = models.BooleanField(default=False)

	def __unicode__(self):
		return "{0} ({1})".format(self.title, self.year)
		