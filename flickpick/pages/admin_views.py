from django.apps import apps
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from pages.models import Page, Widget, PageToWidget
from display.admin_forms import get_widget_form



class WidgetFormView(TemplateView):

	template_name = "admin/display/inline/widget_form.html"

	def get_context_data(self, **kwargs):
		data = super(WidgetFormView, self).get_context_data(**kwargs)

		prefix = self.request.GET.get('prefix', '__prefix__')
		if 'widget_id' in self.request.GET:
			widget = get_object_or_404(Widget, id=self.request.GET['widget_id']).get_subclass()
			if has_attr(widget, 'get_proxied_widget'):
				widget = widget.get_proxied_widget()
			widget_model = type(widget)
		elif 'widget_type_name' in kwargs:
			widget = None
			widget_model = apps.get_model("page", kwargs['widget_type_name'])
		else:
			raise Http404()

		form = get_widget_form(
			widget=model,
			prefix=prefix,
			instance=widget
		)
		data['widget_form'] = form
		return data