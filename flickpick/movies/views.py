from django.shortcuts import render
from django.views.generic import TemplateView

from models import Movie

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

		action_movies = Movie.objects.filter(genre__contains='Adventure')
		context['action_movies'] = action_movies

		dramas = Movie.objects.filter(genre__contains='Drama')
		context['dramas'] = dramas

		comedies = Movie.objects.filter(genre__contains='Comedy')
		context['comedies'] = comedies

		romance_movies = Movie.objects.filter(genre__contains='Romance')
		context['romance_movies'] = romance_movies

		return context
