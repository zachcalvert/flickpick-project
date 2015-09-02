import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User

from models import Movie, Genre
from viewing.models import Viewing

# Create your views here.

def logout(request, template_name='registration/logged_out.html'):
	"""
	Logs the user out and displays the login form
	"""
	logout(request)
	return redirect('site_base.html')


class SeenMovieView(View):

	def dispatch(self, request):
		if request.is_ajax():
			user = request.user

			body = json.loads(request.body)
			movie_id = body.get('movie').strip('movie-')
			
			movie = Movie.objects.get(id=movie_id)

			viewing, created = Viewing.objects.get_or_create(user=user, movie=movie)

			if created:
				d = {'success': 'true', 'viewing': '{0} has seen {1}'.format(user, movie)}
				messages.add_message(self.request, messages.SUCCESS,
					_('{} added to your reel.'.format(movie.title)))
			else:
				d = {'success': 'false'}

			return HttpResponse(json.dumps(d))


class BrowseView(TemplateView):
	template_name = 'browse.html'

	def get_context_data(self, **kwargs):
		context = super(BrowseView, self).get_context_data(**kwargs)

		action = Genre.objects.get(name='Adventure')
		action_movies = action.movie_set.order_by('-year')[:12]
		context['action_movies'] = action_movies

		drama = Genre.objects.get(name='Drama')
		dramas = drama.movie_set.order_by('-year')[:12]
		context['dramas'] = dramas

		comedy = Genre.objects.get(name='Comedy')
		comedies = comedy.movie_set.order_by('-year')[:12]
		context['comedies'] = comedies

		romance = Genre.objects.get(name='Romance')
		romance_movies = romance.movie_set.order_by('-year')[:12]
		context['romance_movies'] = romance_movies

		context['genres'] = Genre.objects.all()

		return context

class GenreView(TemplateView):
	template_name= 'genre.html'

	def get_context_data(self, **kwargs):
		context = super(GenreView, self).get_context_data(**kwargs)

		genre = Genre.objects.get(id=kwargs['genre_id'])
		movies = genre.movie_set.order_by('-year')[:13]
		award_winners = genre.movie_set.filter(notes__isnull=False)[:13]

		context['genre'] = genre
		context['movies'] = movies
		context['award_winners'] = award_winners

		return context


