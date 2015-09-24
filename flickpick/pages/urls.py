from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

import views

API_CACHE = getattr(settings, 'API_DISPLAY_CACHE_TIME', 60*5)

urlpatterns = [
	url(r'^reel/?$', login_required(views.UserReelView.as_view()), name='user_reel_view'),
	
	url(r'^genre/(?P<genre_id>\d+)', login_required(views.GenreWrapperView.as_view()), name='genre_wrapper'),
	url(r'^movie/(?P<movie_id>\w+)', login_required(views.MovieWrapperView.as_view()), name='movie_wrapper'),
	url(r'^person/(?P<person_id>\d+)', login_required(views.PersonWrapperView.as_view()), name='person_wrapper'),

	url(r'^(?P<page_slug>.+)/?$', login_required(cache_page(API_CACHE)(views.SlugPageWrapperView.as_view())), name='slug_page_wrapper'),
	url(r'^(?P<page_path>.+)/?$', login_required(views.WebPageWrapperView.as_view()), name='web_page_wrapper'),
]