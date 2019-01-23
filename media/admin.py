from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Auteur, Emprunt, Media, Jeu


@admin.register(Auteur)
class AuteurAdmin(VersionAdmin):
    list_display = ('nom',)


@admin.register(Media)
class MediaAdmin(VersionAdmin):
    list_display = ('titre', 'cote')


@admin.register(Emprunt)
class EmpruntAdmin(VersionAdmin):
    list_display = (
        'media', 'user', 'date_emprunt', 'date_rendu', 'permanencier_emprunt',
        'permanencier_rendu')


@admin.register(Jeu)
class JeuAdmin(VersionAdmin):
    list_display = (
        'nom', 'proprietaire', 'duree', 'nombre_joueurs_min',
        'nombre_joueurs_max',
        'comment')
