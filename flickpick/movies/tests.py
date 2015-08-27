from django.test import TestCase

from models import Movie, Director, Actor, Writer

def make_movie(title, year=None, genre=None, director=None, actors=None, 
	writers=None, plot=None, poster_url=None, imdb_id=None, imdb_rating=None, **extra):
    
    if not year:
        year = "2000"
    if not genre:
        genre = 'comedy'

	if not director:
		director = Director.objects.create(name="Judy Bloom")

	if not actors:
		Actor.objects.create(name="Dustin Baguette")
		actors = Actor.objects.all()

	if not writers:
		Writer.objects.create(name="Dominic Croissant")
		writers = Writer.objects.all()

	imdb_id = "imdb_id"
	imdb_rating=10.0

	movie = Movie.objects.create(title=title, year=year, genre=genre, director=director,
		plot=plot, poster_url=poster_url, imdb_id=imdb_id)

    return Movie.objects.get(id=movie.id)