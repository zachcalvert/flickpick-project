import json

from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.core.urlresolvers import reverse, Resolver404, resolve
from django.template.response import TemplateResponse
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.http import Http404, HttpResponse


from models import Page
from movies.models import Movie, Person, Genre
from viewing.models import Viewing


class PageView(TemplateView):
	template_name = 'page.json'

	def get_context_data(self, **kwargs):
		context = super(PageView, self).get_context_data(**kwargs)

		if kwargs.get('page_slug'):
			page = Page.objects.get(slug=kwargs['page_slug'])
		else:
			try:
				page = Page.objects.get(id=kwargs['page_id'])
			except KeyError:
				return 'what'

		context['page'] = page

		return context


class WebPageWrapperView(TemplateView):
    template_name = "pages/page.html"
    context_object_name = "page"
    url_namespace = 'pages.api_urls'

    def get_api_url(self, page_path, *args, **kwargs):
        return u"/pages/" + page_path.strip('/') + u".json"

    def dispatch(self, request, *args, **kwargs):
        try:
            resolver_match = resolve(self.get_api_url(*args, **kwargs), self.url_namespace)
        except Resolver404:
            raise Http404

        request.META['HTTP_X_DHDEVICEOS'] = 'web'
        response = resolver_match.func(request, *resolver_match.args, **resolver_match.kwargs)
        if response.status_code >= 400:
            return response

        # working solution
        if isinstance(response, TemplateResponse):
            response.render()

        print response.status_code

        self.page_data = json.loads(response.content)
        for widget in self.page_data.get('widgets', []):
            template_name = "widgets/{}.html".format(widget['type'])
            try:
                get_template(template_name)
            except TemplateDoesNotExist:
                pass
            else:
                widget['template_name'] = template_name

        return super(WebPageWrapperView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WebPageWrapperView, self).get_context_data(**kwargs)
        context[self.context_object_name] = self.page_data
        return context


class SlugPageWrapperView(WebPageWrapperView):
    page_slug = None

    def get_api_url(self, page_slug=None, *args, **kwargs):
        page_slug = page_slug or self.page_slug
        return reverse('page', kwargs={'page_slug': page_slug}, urlconf='pages.api_urls')


class UserReelView(TemplateView):
    template_name = 'pages/user_reel.html'

    def get_context_data(self, **kwargs):
        context = super(UserReelView, self).get_context_data(**kwargs)

        movies = Viewing.objects.all_movies_for_user(self.request.user)

        try:
            page_num = int(self.request.GET.get('page', 1))
        except ValueError:
            page_num = 1

        pager = Paginator(movies, 25)

        try:
            movies = pager.page(page_num)
        except (EmptyPage, InvalidPage):
            movies = pager.page(pager.num_pages)

        context['paginator'] = pager
        context['user_movies'] = movies

        return context


class MovieWrapperView(WebPageWrapperView):
    template_name = "pages/movie_profile.html"
    context_object_name = "movie"

    def get_api_url(self, movie_id, *args, **kwargs):
        return reverse('movie', kwargs={'movie_id': movie_id}, urlconf='pages.api_urls')


class PersonWrapperView(WebPageWrapperView):
    template_name = "pages/person_profile.html"
    context_object_name = "person"

    def get_api_url(self, person_id, *args, **kwargs):
        return reverse('person', kwargs={'person_id': person_id}, urlconf='pages.api_urls')


class MovieView(View):
    def movie_data(self, movie):
        movie_dict = {
            'id': movie.id,
            'title': movie.title,
            'year': movie.year,
            'rated': movie.rated,
            'plot': movie.plot,
            'imdb_id': movie.imdb_id,
            'imdb_rating': str(movie.imdb_rating),
            'notes': movie.notes,
            'on_netflix': movie.on_netflix,
            'on_amazon': movie.on_amazon,
            'on_hulu': movie.on_hulu,

            'image': {
                'url': movie.poster_url,
            },

            'genres': [{
                             'name': g.name,
                             'path': g.get_api_url(),
                         } for g in movie.genres.all()],
            'directors': [{
                           'name': d.person.name,
                           'path': d.person.get_api_url(),
                       } for d in movie.directors.all()],
            'actors': [{
                           'name': a.person.name,
                           'path': a.person.get_api_url(),
                       } for a in movie.actors.all()],
            'writers': [{
                           'name': w.person.name,
                           'path': w.person.get_api_url(),
                       } for w in movie.writers.all()],
            'related': self.get_related(movie),
        }

        return movie_dict

    def get_related(self, movie):
        related_movies = movie.related()

        return [{
            'type': "row_focus",
            'item_type': "movie",
            'title': "Similar Movies",
            'items': [{
                           'id': m.id,
                           'title': m.title,
                           'path': m.get_absolute_url(),
                           'image': {
                                'url': m.poster_url,
                            },
                           'year': m.year,
                       } for m in related_movies ]
        }]

    def get(self, request, movie_id):
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            raise Http404()

        api_dict = self.movie_data(movie)

        return HttpResponse(json.dumps(api_dict))


class PersonView(View):
    def person_data(self, person):
        person_dict = {
            'id': person.id,
            'name': person.name,
            'movies': person.movies(), 
        }

        return person_dict


    def get(self, request, person_id):
        try:
            person = Person.objects.get(id=person_id)
        except Person.DoesNotExist:
            raise Http404()

        api_dict = self.person_data(person)

        return HttpResponse(json.dumps(api_dict))


class GenreView(View):
    def genre_data(self, genre):
        genre_dict = {
            'id': genre.id,
            'name': genre.name,
            'movies': genre.movies(), 
        }

        return genre_dict


    def get(self, request, genre_id):
        try:
            genre = Genre.objects.get(id=genre_id)
        except Person.DoesNotExist:
            raise Http404()

        api_dict = self.genre_data(genre)

        return HttpResponse(json.dumps(api_dict))



