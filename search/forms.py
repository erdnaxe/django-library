from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.utils.translation import gettext_lazy as _

CHOICES = (
    ('0', 'Actifs'),
    ('1', 'Désactivés'),
    ('2', 'Archivés'),
)

CHOICES2 = (
    ('0', 'Utilisateurs'),
    ('1', 'Media'),
    ('2', 'Emprunts'),
    ('3', 'Jeu'),
)


class SearchForm(forms.Form):
    search_field = forms.CharField(
        label='Search',
        max_length=100
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Search')))


class AdvancedSearchForm(SearchForm):
    search_field = forms.CharField(
        label='Search',
        max_length=100,
        required=False
    )
    filtre = forms.MultipleChoiceField(
        label="Filtre utilisateurs",
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=CHOICES
    )
    affichage = forms.MultipleChoiceField(
        label="Filtre affichage",
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=CHOICES2
    )
    date_deb = forms.DateField(
        required=False,
        label="Date de début",
        help_text='DD/MM/YYYY',
        input_formats=['%d/%m/%Y']
    )
    date_fin = forms.DateField(
        required=False,
        help_text='DD/MM/YYYY',
        input_formats=['%d/%m/%Y'],
        label="Date de fin"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Search')))
