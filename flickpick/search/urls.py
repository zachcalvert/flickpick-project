from django.conf.urls import url
from search.views import SearchPage

urlpatterns = (
    # TODO : html-ify this page object
    url(r'^search.html/?$', SearchPage.as_view(), name='search_html'),
)