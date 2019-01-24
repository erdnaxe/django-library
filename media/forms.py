from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import Auteur, Media, Jeu, Emprunt


class AuteurForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Appliquer'))

    class Meta:
        model = Auteur
        fields = '__all__'


class MediaForm(forms.ModelForm):
    auteur = forms.ModelMultipleChoiceField(
        Auteur.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Appliquer'))

    class Meta:
        model = Media
        fields = '__all__'


class JeuForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Appliquer'))

    def clean_nombre_joueurs_max(self):
        if self.cleaned_data['nombre_joueurs_max'] < self.cleaned_data[
            'nombre_joueurs_min']:
            raise forms.ValidationError("Max ne peut être inférieur à min")
        return self.cleaned_data['nombre_joueurs_max']

    class Meta:
        model = Jeu
        fields = '__all__'


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
