from haystack.forms import SearchForm, model_choices
from django import forms
from django.utils.translation import ugettext_lazy as _

class FlickpickSearchForm(SearchForm):

    def __init__(self, *args, **kwargs):
        super(FlickpickSearchForm, self).__init__(*args, **kwargs)
        self.fields['models'] = forms.MultipleChoiceField(
            choices=model_choices(),
            required=False,
            label=_('Search In'),
            widget=forms.CheckboxSelectMultiple
        )

    def search(self):
        sqs = super(FlickpickSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        return sqs