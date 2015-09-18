import json

from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_protect

from models import Movie, Genre
from viewing.models import Viewing


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
					_('{} has been added to your reel.'.format(movie.title)))
			else:
				d = {'success': 'false'}

			return HttpResponse(json.dumps(d))


class RatedMovieView(View):

	def dispatch(self, request):
		if request.is_ajax():
			user = request.user

			body = json.loads(request.body)
			movie_id = body.get('movie').strip('movie-')
			rating = body.get('rating')
			
			movie = Movie.objects.get(id=movie_id)
			viewing = Viewing.objects.get(user=user, movie=movie)
			viewing.rating = rating
			viewing.save()

			d = {'success': 'true', 'movie': '{0} has been rated {1}'.format(movie, rating)}
			return HttpResponse(json.dumps(d))
