from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.apps import apps
from django import forms
from django.http import Http404
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy

from pages.admin_forms import PageForm, get_widget_form
from pages.admin_views import WidgetFormView, WidgetNameLookupView, WidgetPageLookupView

import pages.views
from pages.models import Page
from pages.templatetags.page_tags import admin_url
from grappelli.forms import GrappelliSortableHiddenMixin
from movies.models import Movie, Genre, Director, Actor, Writer
from flickpick_utils.admin import SortedManyToManyAdmin, AjaxModelAdmin
from flickpick_utils.widgets import FilteredSelect

WIDGET_MODELS = [model for model in apps.get_models(pages.models)
                 if issubclass(model, pages.models.Widget) and model != pages.models.Widget]


class DefaultNullBooleanSelect(forms.NullBooleanSelect):
    def __init__(self, attrs=None):
        choices = (('1', ugettext_lazy('Default')),
                   ('2', ugettext_lazy('Yes')),
                   ('3', ugettext_lazy('No')))
        super(forms.NullBooleanSelect, self).__init__(attrs, choices)


class SaveAsNewAdmin(admin.ModelAdmin):
    save_as = True

    def response_add(self, request, obj, post_url_continue=None):
        """
        Workaround for https://code.djangoproject.com/ticket/16327:
        django admin bug that causes the user to be redirected back to change_list on save as new,
        instead of the newly created object's change view.
        """
        if "_saveasnew" in request.POST:
            request.POST['_continue'] = True
        return super(SaveAsNewAdmin, self).response_add(request, obj=obj, post_url_continue=post_url_continue)


class PageAdmin(SortedManyToManyAdmin, SaveAsNewAdmin):
    search_fields = ['name', 'slug']
    list_display = ['name', 'url', 'created', 'last_modified', 'draft']
    list_filter = ['slug', 'draft']
    date_hierarchy = 'created'
    readonly_fields = ('created', 'last_modified')
    fieldsets = (
        (None, {
            'fields': ('name', ('created', 'last_modified', 'slug'), 'draft')
        }),
    )
    form = PageForm
    formfield_overrides = {
        models.NullBooleanField: {'widget': DefaultNullBooleanSelect},
        models.ForeignKey: {'widget': FilteredSelect},
    }

    class Media:
        js = AjaxModelAdmin.Media.js + (
            "js/admin/pages/page.js",
            "js/jquery.typewatch.js",
            "js/FilteredSelect.js",
            "js/admin/pages/generic_lookup.js",
        )
        css = {
            "all": (
                "css/admin/pages/page/change.css",
                "css/filtered_select.css",
                "css/admin/pages/generic_lookup.css",
            )
        }

    def url(self, page):
        return mark_safe(u"<a href='{0}' target='_new'>{0}</a>".format(page.get_api_url()))

    def get_urls(self):
        from django.conf.urls import url

        app_name = self.model._meta.app_label
        model_name = self.model._meta.model_name

        urlpatterns = [
            url(r'^widget_form/$',
                self.admin_site.admin_view(WidgetFormView.as_view()),
                name='{}_{}_widget_form'.format(app_name, model_name)),
            url(r'^widget_form/(?P<widget_type_name>\w+)/$',
                self.admin_site.admin_view(WidgetFormView.as_view()),
                name='{}_{}_widget_form'.format(app_name, model_name)),
            url(r'^widget_name_lookup/$',
                self.admin_site.admin_view(WidgetNameLookupView.as_view()),
                name='{}_{}_widget_name_lookup'.format(app_name, model_name)),
            url(r'^widget_page_name_lookup/$',
                self.admin_site.admin_view(WidgetPageLookupView.as_view()),
                name='{}_{}_widget_page_name_lookup'.format(app_name, model_name)),
            url(r'^generate_for_object/ct_(?P<content_type_id>\d+)/(?P<obj_id>\d+)/',
                self.admin_site.admin_view(self.generate_page_view),
                name='{}_{}_generate_page'.format(app_name, model_name)),
        ] + super(PageAdmin, self).get_urls()
        return urlpatterns

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context['form'] = context['adminform'].form
        context['widget_types'] = [w._meta for w in WIDGET_MODELS]

        # set up "will replace" warnings for slug dropdown
        slug_pages = Page.objects.filter(slug__isnull=False)
        if obj:
            slug_pages = slug_pages.exclude(pk=obj.pk)
        context['slug_pages'] = slug_pages

        return super(PageAdmin, self).render_change_form(request, context, add, change, form_url, obj)

    def save_form(self, request, form, change):
        return form.save(commit=True)

    def generate_page_view(self, request, content_type_id, obj_id):
        ct = ContentType.objects.get(id=content_type_id)
        obj = ct.get_object_for_this_type(pk=obj_id)

        if isinstance(obj, Movie):
            obj = obj

        view_lookups = [
            (Genre,          pages.views.AutoGenreView()),
        ]

        for model, view in view_lookups:
            if isinstance(obj, model):
                view.request = request
                if isinstance(view, pages.views.AutoGroupView):
                    lookup_id = obj.uuid
                    if not isinstance(lookup_id, (str, unicode)):
                        lookup_id = lookup_id.value
                else:
                    lookup_id = obj.id
                dummy_page = view.get_page(lookup_id)
                break
        else:
            raise Http404()

        page = Page.objects.create(name=dummy_page.name)
        for widget in dummy_page.widgets:
            widget.save()
            page.add_widget(widget)
        obj.page = page
        obj.save()

        return redirect("admin:pages_page_change", page.id)


admin.site.register(Page, PageAdmin)


class GroupWidgetAdmin(admin.ModelAdmin):
    search_fields = ["name", "pages__name"]
    list_display = ["name", "page_links"]
    readonly_fields = ['page_links']
    exclude = [
        'link_id',
        'link_type',

        'source_genre',
        'source_director',
        'source_actor',
        'source_writer',
        'source_year',
    ]
    default_exclude = [
        'name',
        'start_date',
        'end_date',
        'page_links',
        'link',
        'source',

        'movie',
    ]
    change_form_template = "admin/pages/widget_change_form.html"

    class Media:
        js = AjaxModelAdmin.Media.js + (
            "js/admin/pages/page.js",
            "js/jquery.typewatch.js",
        )
        css = {
            "all": (
                "css/admin/pages/widget/change.css",
            )
        }

    def get_form(self, request, obj=None, **kwargs):
        kwargs['form'] = type(get_widget_form(self.model, inline=False))
        return super(GroupWidgetAdmin, self).get_form(request, obj=obj, **kwargs)

    def save_form(self, request, form, change):
        return form.save(commit=True)

    def page_links(self, widget):
        output = ["<ul>"]

        for page in widget.pages.all():
            output.append("<li>")
            output.append("<a href='{url}'>{label}</a>".format(
                url=admin_url(page),
                label=page.name
            ))
            output.append("</li>")

        output.append("</ul>")
        return mark_safe(" ".join(output))
    page_links.short_description = "pages"


for model in WIDGET_MODELS:
    try:
        admin.site.register(model, GroupWidgetAdmin)
    except AlreadyRegistered:
        pass
