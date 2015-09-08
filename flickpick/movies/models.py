from django.db import models

from django.core.urlresolvers import reverse


# class MovieGroupModel(NameOverrideModel):

#     page = models.ForeignKey('pages.Page', null=True, blank=True, on_delete=models.SET_NULL)
#     banner_widget = models.ForeignKey('pages.BannerWidget', null=True, blank=True, on_delete=models.SET_NULL,
#                                       help_text='Banner at the top of automatic pages')
#     text_widget = models.ForeignKey('pages.TextWidget', null=True, blank=True, on_delete=models.SET_NULL,
#                                     help_text='Text widget near the top of automatic pages')
#     ongoing = models.BooleanField(default=False)

#     def get_api_url(self):
#         return reverse("group", args=[self.id])

#     class Meta:
#         abstract = True


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

	def movies(self):
		return [m.title for m in self.movie_set.all()]

	def get_api_url(self):
		return reverse('genre', kwargs={'genre_id': self.pk})	

	def get_absolute_url(self):
		return reverse('genre_browse', kwargs={'genre_id': self.pk})

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


	class Meta():
		ordering = ('title', '-year')


	def __unicode__(self):
		return "{0} ({1})".format(self.title, self.year)

	def get_api_url(self):
		return reverse('movie', kwargs={'movie_id': self.pk})

	def get_absolute_url(self):
		return reverse('movie_wrapper', kwargs={'movie_id': self.pk})

	def related(self):
		return Movie.objects.filter(genres__in=self.genres.all).distinct()[:10]
		