from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import Emprunt


class EmpruntForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Appliquer'))

    class Meta:
        model = Emprunt
        fields = ['media']


class EditEmpruntForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Appliquer'))

    class Meta:
        model = Emprunt
        fields = ['media', 'permanencier_emprunt', 'permanencier_rendu',
                  'date_rendu']
