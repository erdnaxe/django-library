from django import forms
from django.forms import ModelForm

from .models import Adhesion, User


class BaseInfoForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
        ]


class InfoForm(BaseInfoForm):
    class Meta(BaseInfoForm.Meta):
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'max_borrowed',
        ]


class StateForm(ModelForm):
    class Meta:
        model = User
        fields = ['state']


class AdhesionForm(ModelForm):
    adherent = forms.ModelMultipleChoiceField(
        User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Adhesion
        fields = '__all__'
