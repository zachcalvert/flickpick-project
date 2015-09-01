from django.shortcuts import render

from django.views.generic import TemplateView

from models import Page

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