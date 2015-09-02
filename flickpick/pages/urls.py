from django.conf.urls import url
import views

urlpatterns = [
	url(r'^movie/(?P<movie_id>\w+)', views.MovieProfileView.as_view(), name='movie_profile'),
	url(r'^(?P<page_path>.+)/?$', views.WebPageWrapperView.as_view(), name='web_page_wrapper'),
]