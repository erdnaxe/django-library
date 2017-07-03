# Re2o est un logiciel d'administration développé initiallement au rezometz. Il
# se veut agnostique au réseau considéré, de manière à être installable en
# quelques clics.
#
# Copyright © 2017  Gabriel Détraz
# Copyright © 2017  Goulven Kermarec
# Copyright © 2017  Augustin Lemesle
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from django.forms import ModelForm, Form, ValidationError
from django import forms
from .models import Auteur, Media, Jeu, Emprunt

class AuteurForm(ModelForm):
    class Meta:
        model = Auteur
        fields = '__all__'

class MediaForm(ModelForm):
    class Meta:
        model = Media
        fields = '__all__'

class JeuForm(ModelForm):
    class Meta:
        model = Jeu
        fields = '__all__'

class EmpruntForm(ModelForm):
    class Meta:
        model = Emprunt
        fields = ['media']

class EditEmpruntForm(ModelForm):
    class Meta:
        model = Emprunt
        fields = ['media', 'permanencier_emprunt', 'permanencier_rendu', 'date_rendu']
