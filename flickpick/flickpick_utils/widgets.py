from bs4 import BeautifulSoup
from django.contrib.admin.templatetags.admin_static import static
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.urlresolvers import reverse
from django.forms import Select, TextInput
from django.utils.safestring import mark_safe
from django.conf import settings


class OrderedFilteredSelectMultiple(FilteredSelectMultiple):

    @property
    def media(self):
        media = super(OrderedFilteredSelectMultiple, self).media
        media.add_js([static("js/OrderedSelectFilter.js")])
        if 'grappelli' in settings.INSTALLED_APPS:
            media.add_css({'all': [static("css/ordered_select_grappelli.css")]})
        else:
            media.add_css({'all': [static("css/ordered_select.css")]})
        return media

    def render(self, name, value, attrs=None, choices=()):
        rendered = super(OrderedFilteredSelectMultiple, self).render(name, value, attrs=attrs, choices=choices)

        if type(value) in (list, tuple) and len(value) > 0:
            # sort the selected values
            soup = BeautifulSoup(rendered)
            select = soup.find('select')
            for v in reversed(value):
                option = soup.find('option', {'value': v})
                option.extract()
                select.insert(0, option)

            rendered = unicode(soup)

        rendered = rendered.replace(u"SelectFilter.init(", u"OrderedSelectFilter.init(")
        return mark_safe(rendered)


class FilteredSelect(Select):

    class Media:
        js = [static("js/FilteredSelect.js")]
        css = {'all': [static("css/filtered_select.css")]}

    def render(self, *args, **kwargs):
        attrs = kwargs.setdefault('attrs', {})
        css_class = attrs.setdefault('class', '')+" filtered-select"
        attrs['class'] = css_class
        rendered = super(FilteredSelect, self).render(*args, **kwargs)
        return mark_safe(rendered)