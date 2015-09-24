from urllib import quote_plus

from django.core.urlresolvers import reverse
from django.utils.html import escapejs
from django.core.cache import cache

from haystack.query import SearchQuerySet

from movies.models import Movie, Person
from display.models import Page
from display.views import PageView
from search.forms import FlickpickSearchForm
from django.conf import settings


class SpellingSuggestionView(View):
    """
    Spelling suggestion endpoint
    If this endpoint isn't working, ensure that you have "INCLUDE_SPELLING" in your
    haystack configuration.
    """

    def get(self, request):
        query_terms = request.GET.get('q', '')
        return [
            "{}".format(SearchQuerySet().spelling_suggestion(query_terms))
        ]


class AutocompleteView(View):
    """
    Auto complete endpoint
    Provides a list of dictionaries of list of completion recommendations, by movie and person
    """

    def get(self, request):
        query_terms = request.GET.get('q', '')
        limit = int(request.GET.get('l', 10))

        movie_autocomplete_list = []
        person_autocomplete_list = []

        if query_terms != '':
            movie_autocomplete_list = [m.title for m in
                                             SearchQuerySet().autocomplete(name=query_terms).models(
                                                 Movie)[:limit] if m]
            person_autocomplete_list = [p.name for p in
                                        SearchQuerySet().autocomplete(name=query_terms).models(Person)[
                                        :limit] if p]

        return [
            {'movie': movie_autocomplete_list, },
            {'person': person_autocomplete_list, },
        ]


def raw_search(request):
    """
    Returns a data-y view of the search
    TODO: passing in template value of None should return a darkhorse 'Page' object with a list of
    books, groups, and contributors displayed as search result widgets (maybe?)
    """
    search_results = {}
    maximum_search_results = 1000

    if request.GET.get('q'):
        queryset = SearchQuerySet()
        form = FlickpickSearchForm(request.GET, searchqueryset=queryset, load_all=True)
        limit = int(request.GET.get('l', settings.HAYSTACK_SEARCH_RESULTS_LIMIT_PER_CATEGORY))

        if limit < 0:
            limit = maximum_search_results

        if form.is_valid():
            # We're gonna separate out the models information and do it manually below
            # to separate out the results by class
            scope = form.cleaned_data['models']
            form.cleaned_data['models'] = []

            # assume all models if not specified otherwise
            if not scope:
                scope = ['movies.movie', 'movies.person']

            results = form.search()

            if 'movies.movie' in scope:
                search_results['movies.movie'] = [
                    m for m in results.models(Movie)[:limit] if m is not None
                ]

            if 'movies.person' in scope:
                search_results['movies.person'] = [
                    p for p in results.models(Person)[:limit] if p is not None
                ]

            query_terms = request.GET.get('q', '')
            search_results['query'] = query_terms

            if results.query.backend.include_spelling:
                search_results['suggestion'] = form.get_suggestion()

    return search_results


class SearchPage(PageView):
    """
    use the raw search function to generate a page of results
    """

    def get_page(self, **kwargs):
        query_terms = self.request.GET.get('q', '')

        page_name = escapejs(u"Searching for: '{}'".format(query_terms)) if query_terms else "Search"

        page = Page(
            name=page_name,
        )

        widget_list = self.generate_widgets(query_terms)
        page.widgets = widget_list
        return page

    def generate_widgets(self, query_terms):
        widget_list = []
        search_results = raw_search(self.request)

        if 'movies.movie' in search_results and search_results['movies.movie']:
            group_dict = {
                'template_name': 'widgets/group.json',
                'display_type': 'gallery',
                'item_type': 'group',
                'group': {
                    'type': 'group',
                },
                'name': "Movies",
                'limited_items': [
                    m.object for m in search_results['movies.movie']
                ],
                'item_template_name': 'widgets/items/movie.json',
            }

        if 'movies.person' in search_results and search_results['movies.person']:
            contributor_dict = {
                'template_name': 'widgets/group.json',
                'display_type': 'gallery',
                'item_type': 'person',
                'group': {
                    'type': 'person',
                },
                'name': "People",
                'limited_items': [
                    p.object for p in search_results['movies.person']
                ],
                'item_template_name': 'widgets/items/person.json',
            }

        if len(widget_list) == 0:
            if 'suggestion' in search_results and search_results['suggestion'] != None:

                suggest_string = u"No results found."

                # If the search engine doesn't have a dumb recommendation to look for the same thing
                # with a different capitalization, go ahead and add that suggestion.
                if search_results['query'].lower() != search_results['suggestion'].lower():
                    suggest_string = u"{} Try searching for '{}' instead.".format(suggest_string,
                                                                                  search_results['suggestion'])

                widget_list.append({
                    "json_content": escapejs(suggest_string),
                    "text_color": "#000000",
                    "template_name": "widgets/text.json"
                })

        return widget_list

