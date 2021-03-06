from django.conf.urls import url

import views, admin_views

urlpatterns = [
	url(r'^movie/(?P<movie_id>\w+).json$', views.MovieView.as_view(), name='movie'),
	url(r'^person/(?P<person_id>\w+).json$', views.PersonView.as_view(), name='person'),
	url(r'^genre/(?P<genre_id>\w+).json$', views.GenreView.as_view(), name='genre'),

	url(r'^pages/(?P<page_id>\d+).json', views.PageView.as_view(), name="page"),
    url(r'^pages/(?P<page_slug>[a-zA-Z]\w*).json$', views.PageView.as_view(), name="page"),

    url(r'^admin/generic_object_lookup/', admin_views.GenericObjectLookup.as_view(), name='generic_object_lookup'),
]