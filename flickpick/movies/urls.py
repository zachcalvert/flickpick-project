from django.conf.urls import url
from django.views.generic import TemplateView
import views

urlpatterns = [
    url(r'^$', views.BrowseView.as_view(), name="browse"),
    url(r'^genres/(?P<genre_id>\d+)/$', views.GenreView.as_view(), name="genre_browse"),
]