from django.conf.urls import url
from django.views.decorators.cache import cache_page
from django.conf import settings
import views

API_CACHE = getattr(settings, 'API_DISPLAY_CACHE_TIME', 60*5)

urlpatterns = [
	url(r'^reel/?$', views.UserReelView.as_view(), name='user_reel_view'),
	
	url(r'^movie/(?P<movie_id>\w+)', views.MovieWrapperView.as_view(), name='movie_wrapper'),
	url(r'^person/(?P<person_id>\d+)', views.PersonWrapperView.as_view(), name='person_wrapper'),

	url(r'^page/(?P<page_slug>.+)/?$', cache_page(API_CACHE)(views.SlugPageWrapperView.as_view()), name='slug_page_wrapper'),
	url(r'^(?P<page_path>.+)/?$', views.WebPageWrapperView.as_view(), name='web_page_wrapper'),
]