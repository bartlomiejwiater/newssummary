from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class WordsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(WordsForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'id-get-words-list'
        self.helper.form_class = 'blueForms form-horizontal'
        self.helper.form_method = 'GET'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'

        self.helper.add_input(Submit('submit', 'Submit'))

    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)
