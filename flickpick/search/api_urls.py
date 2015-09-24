from django.conf.urls import url

from search import views

urlpatterns = (
    # spelling suggestions
    url(r'^suggest.json/?$', views.SpellingSuggestionView.as_view(), name='search_suggest'),
    url(r'^autocomplete.json/?$', views.AutocompleteView.as_view(), name='search_autocomplete'),
    url(r'^search.json/?$', views.SearchPage.as_view(), name='search_api'),
)

