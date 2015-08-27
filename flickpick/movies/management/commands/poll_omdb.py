import json
import requests

from decimal import Decimal
from movies.movies_list import all_movies
from movies.models import Movie, Director, Actor, Writer

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """
    Polls the omdb API for movie info
    """
    def handle(self, *args, **options):
        for title in all_movies[:50]:
            response = requests.get('http://www.omdbapi.com/?t={}'.format(title))

            if response.status_code == 200:
                d = json.loads(response.content)
                title = d.get('Title')
                year = d.get('Year')
                rated = d.get('Rated')
                # released = d.get('Released')
                genre = d.get('Genre')
                director_name = d.get('Director')
                writer_names = d.get('Writer')
                actor_names = d.get('Actors')
                plot = d.get('Plot')
                notes = d.get('Awards')
                imdb_id = d.get('imdbID')
                imdb_rating = 8.0
                poster_url = d.get("Poster")

                director, created = Director.objects.get_or_create(name=director_name)
                
                writers = []
                for writer_name in writer_names:
                    writer, created = Writer.objects.get_or_create(name=writer_name)
                    writers.append(writer)

                actors = []
                for actor_name in actor_names:
                    actor, created = Actor.objects.get_or_create(name=actor_name)
                    actors.append(actor)

                movie = Movie.objects.create(title=title, year=year, rated=rated, 
                    genre=genre, director=director, plot=plot, notes=notes, 
                    imdb_id=imdb_id, imdb_rating=imdb_rating, poster_url=poster_url)
                print('added movie {} to db'.format(title))

            else:
                print('could not fetch info for {}'.format(title))
