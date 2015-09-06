from django.conf.urls import url
import views

urlpatterns = [
	url(r'^reel/?$', views.UserReelView.as_view(), name='user_reel_view'),
	
	url(r'^movie/(?P<movie_id>\w+)', views.MovieWrapperView.as_view(), name='movie_wrapper'),
	url(r'^person/(?P<person_id>\d+)', views.PersonProfileView.as_view(), name='person_profile'),

	url(r'^page/(?P<page_slug>.+)/?$', views.SlugPageWrapperView.as_view(), name='slug_page_wrapper'),
	url(r'^(?P<page_path>.+)/?$', views.WebPageWrapperView.as_view(), name='web_page_wrapper'),
]