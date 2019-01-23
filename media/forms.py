from django import forms
from django.forms import ModelForm

from .models import Auteur, Media, Jeu, Emprunt


class AuteurForm(ModelForm):
    class Meta:
        model = Auteur
        fields = '__all__'


class MediaForm(ModelForm):
    auteur = forms.ModelMultipleChoiceField(
        Auteur.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Media
        fields = '__all__'


class JeuForm(ModelForm):
    class Meta:
        model = Jeu
        fields = '__all__'

    def clean_nombre_joueurs_max(self):
        if self.cleaned_data['nombre_joueurs_max'] < self.cleaned_data[
            'nombre_joueurs_min']:
            raise forms.ValidationError("Max ne peut être inférieur à min")
        return self.cleaned_data['nombre_joueurs_max']


class EmpruntForm(ModelForm):
    class Meta:
        model = Emprunt
        fields = ['media']


class EditEmpruntForm(ModelForm):
    class Meta:
        model = Emprunt
        fields = ['media', 'permanencier_emprunt', 'permanencier_rendu',
                  'date_rendu']
