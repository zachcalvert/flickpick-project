from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

import views

urlpatterns = [
    url(r'^seen/$', csrf_exempt(views.SeenMovieView.as_view()), name="user_seen_movie"),
    url(r'^rated/$', csrf_exempt(views.RatedMovieView.as_view()), name="user_rated_movie"),    
]