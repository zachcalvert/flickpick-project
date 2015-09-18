from django.contrib import admin
from django.contrib.admin.utils import unquote
from django.contrib.admin.validation import BaseValidator
from django.contrib.messages import get_messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.contrib.admin.widgets import FilteredSelectMultiple

from flickpick_utils.fields import SortedManyToManyField
from pages.views import JSONHttpResponse


class AjaxModelAdmin(admin.ModelAdmin):
    class Media:
        js = (
            "js/jquery.admin-compat.js",
            "js/admin/flickpick.js",
        )
        css = {
             'all': ('css/flickpick.css',)
        }

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        request.form_instance = context['adminform'].form
        return super(AjaxModelAdmin, self).render_change_form(request, context, add, change, form_url, obj)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        response = super(AjaxModelAdmin, self).change_view(request, object_id, form_url, extra_context)
        if request.is_ajax():
            messages = get_messages(request)
            response_json = {"messages": [{'level': m.level, 'message': m.message, 'tags': m.tags} for m in messages],
                             'errors': {}}
            if hasattr(request, 'form_instance') and not request.form_instance.is_valid():
                response_json['errors'].update(request.form_instance.errors)
            # add inline_formset errors
            # TODO This could potentially trigger a bug in future django. context_data is not guaranteed to be there.
            if hasattr(response, 'context_data'):
                for formset in response.context_data['inline_admin_formsets']:
                    for form in formset.formset.forms:
                        if not form.is_valid():
                            for field, error in form.errors.iteritems():
                                response_json['errors']["{}-{}".format(form.prefix, field)] = error
            return JSONHttpResponse(response_json)
        else:
            return response


class SortedManyToManyAdminValidator(BaseValidator):
    def check_field_spec(self, cls, model, flds, label):
        """
        Remove SortedManyToManyField instances from flds before actual validation (they're ok)

        The BaseValidator doesn't allow ManyToManyFields which specify a through model (that isn't auto_created)
        For now (until we automatically create the through table for SortedManyToManyFields) we'll just suppress that
        validation error, and trust that the through model doesn't have any more extra magical stuff on it.
        """
        ok_flds = []
        for fields in flds:
            if type(fields) != tuple:
                fields = (fields,)
            ok_fields = []
            for field in fields:
                try:
                    f = model._meta.get_field(field)
                except models.FieldDoesNotExist:
                    f = None
                if not isinstance(f, SortedManyToManyField):
                    ok_fields.append(field)
            ok_flds.append(tuple(ok_fields))
        ok_flds = tuple(ok_flds)
        super(SortedManyToManyAdminValidator, self).check_field_spec(cls, model, ok_flds, label)


class SortedManyToManyAdmin(AjaxModelAdmin):
    validator_class = SortedManyToManyAdminValidator

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if isinstance(db_field, SortedManyToManyField):
            kwargs['widget'] = FilteredSelectMultiple(verbose_name=db_field.verbose_name, is_stacked=False)
            return db_field.formfield(**kwargs)
        else:
            return super(SortedManyToManyAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
