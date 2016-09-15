from django import forms
from django.contrib.sites.models import Site
from django_select2.forms import HeavySelect2MultipleWidget, HeavySelect2TagWidget
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ChoiceFieldNoValidation(forms.MultipleChoiceField):

    def validate(self, value):
        pass


class WordsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(WordsForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'id-get-words-list'
        self.helper.form_class = 'blueForms form-horizontal'
        self.helper.form_method = 'get'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'

        self.helper.add_input(Submit('submit', 'Submit'))

    words = ChoiceFieldNoValidation(
        widget=HeavySelect2MultipleWidget(data_view='words-select'),
        required=False)
    start_date = forms.DateTimeField(input_formats='%Y-%m-%d', required=False)
    end_date = forms.DateTimeField(input_formats='%Y-%m-%d', required=False)
