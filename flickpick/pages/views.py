import json

from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse, Resolver404, resolve
from django.template.response import TemplateResponse
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.http import Http404


from models import Page
from movies.models import Movie


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

    def get_context_data(self, **kwargs):
        context = super(SlugPageWrapperView, self).get_context_data(**kwargs)
        if kwargs.get('page_slug') == 'series':
            context['all_series'] = Series.objects.filter_approved()
        return context


class MovieProfileView(TemplateView):
    template_name = "pages/movie_profile.html"

    def get_context_data(self, movie_id, **kwargs):
        context = super(MovieProfileView, self).get_context_data(**kwargs)
        context['movie'] = Movie.objects.get(id=movie_id)
        return context

