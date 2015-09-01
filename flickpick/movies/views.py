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


