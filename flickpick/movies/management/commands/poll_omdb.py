import json
import requests

from decimal import Decimal
from movies.movies_list import all_movies
from movies.models import Movie, Director, Actor, Writer, Genre, Person

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """
    Polls the omdb API for movie info
    """
    def handle(self, *args, **options):
        for title in all_movies:
            response = requests.get('http://www.omdbapi.com/?t={}'.format(title))

            if response.status_code == 200:
                d = json.loads(response.content)
                title = d.get('Title')
                year = d.get('Year')
                rated = d.get('Rated')
                # released = d.get('Released')
                genre_names = d.get('Genre')
                director_names = d.get('Director')
                writer_names = d.get('Writer')
                actor_names = d.get('Actors')
                plot = d.get('Plot')
                notes = d.get('Awards')
                imdb_id = d.get('imdbID')
                imdb_rating = 8.0
                poster_url = d.get("Poster")

                if plot is not None:
                    plot = plot[:299]

                if title is None:
                    continue

                movie, created = Movie.objects.get_or_create(title=title, year=year, rated=rated, 
                    plot=plot, notes=notes, imdb_id=imdb_id, poster_url=poster_url)
                print('added movie {} to db'.format(title))

                writers = [x.strip() for x in writer_names.split(',')]
                for writer in writers:
                    # rip out the role
                    writer_name, sep, role = writer.partition(' (')
                    role = role[:-1] # remove the end parentheses

                    person, created = Person.objects.get_or_create(name=writer_name)
                    writer, created = Writer.objects.get_or_create(person=person)
                    movie.writers.add(writer)
                    print('added writer {0} to movie {1}'.format(writer, movie))

                actors = [x.strip() for x in actor_names.split(',')]
                for actor_name in actors:
                    person, created = Person.objects.get_or_create(name=actor_name)
                    actor, created = Actor.objects.get_or_create(person=person)
                    movie.actors.add(actor)
                    print('added actor {0} to movie {1}'.format(actor, movie))

                genres = [x.strip() for x in genre_names.split(',')]
                for genre in genres:
                    genre, created = Genre.objects.get_or_create(name=genre)
                    movie.genres.add(genre)
                    print('added genre {0} to movie {1}'.format(genre, movie))

                directors = [x.strip() for x in director_names.split(',')]
                for director in directors:
                    person, created = Person.objects.get_or_create(name=director)
                    director, created = Director.objects.get_or_create(person=person)
                    movie.directors.add(director)
                    print('added director {0} to movie {1}'.format(director, movie))


            else:
                print('could not fetch info for {}'.format(title))
