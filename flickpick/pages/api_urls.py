from django.conf.urls import url
import views

urlpatterns = [
	url(r'^movies/(?P<movie_id>\w+).json$', views.MovieView.as_view(), name='movie'),

	url(r'^pages/(?P<page_id>\d+).json', views.PageView.as_view(), name="page"),
    url(r'^pages/(?P<page_slug>[a-zA-Z]\w*).json$', views.PageView.as_view(), name="page"),
]