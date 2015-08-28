from django.shortcuts import render
from django.views.generic import TemplateView

from models import Movie, Genre

# Create your views here.

def logout(request, template_name='registration/logged_out.html'):
	"""
	Logs the user out and displays the login form
	"""
	logout(request)
	return redirect('site_base.html')


class BrowseView(TemplateView):
	template_name = 'browse.html'

	def get_context_data(self, **kwargs):
		context = super(BrowseView, self).get_context_data(**kwargs)

		adventure = Genre.objects.get(name='Adventure')
		action_movies = Movie.objects.filter(genres__in=[adventure.id])
		context['action_movies'] = action_movies

		drama = Genre.objects.get(name='Drama')
		dramas = Movie.objects.filter(genres__in=[drama.id])
		context['dramas'] = dramas

		comedy = Genre.objects.get(name='Comedy')
		comedies = Movie.objects.filter(genres__in=[comedy.id])
		context['comedies'] = comedies

		romance = Genre.objects.get(name='Romance')
		romance_movies = Movie.objects.filter(genres__in=[romance.id])
		context['romance_movies'] = romance_movies

		return context
