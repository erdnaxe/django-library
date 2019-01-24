from django import forms
from django.forms import Form

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


class SearchForm(Form):
    search_field = forms.CharField(
        label='Search',
        max_length=100
    )


class SearchFormPlus(Form):
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
        required=False, help_text='DD/MM/YYYY',
        input_formats=['%d/%m/%Y'],
        label="Date de fin"
    )
