from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
import views

urlpatterns = [
    url(r'^$', views.BrowseView.as_view(), name="browse"),
    url(r'^genres/(?P<genre_id>\d+)/$', views.GenreView.as_view(), name="genre_browse"),

    url(r'^seen/$', csrf_exempt(views.SeenMovieView.as_view()), name="user_seen_movie"),
    url(r'^rated/$', csrf_exempt(views.RatedMovieView.as_view()), name="user_rated_movie"),    
]