from django.conf.urls import url
import views

urlpatterns = [
	url(r'^movie/(?P<movie_id>\d+)', views.MovieProfileView.as_view(), name='movie_profile'),
	url(r'^person/(?P<person_id>\d+)', views.PersonProfileView.as_view(), name='person_profile'),
	url(r'^(?P<page_path>.+)/?$', views.WebPageWrapperView.as_view(), name='web_page_wrapper'),
]