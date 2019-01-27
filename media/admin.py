from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Author, Emprunt, Media, Game


@admin.register(Emprunt)
class BorrowedMediaAdmin(VersionAdmin):
    list_display = (
        'media', 'user', 'date_emprunt', 'date_rendu', 'permanencier_emprunt',
        'permanencier_rendu')


@admin.register(Author)
class AuthorAdmin(VersionAdmin):
    list_display = ('nom',)


@admin.register(Media)
class MediaAdmin(VersionAdmin):
    list_display = ('titre', 'get_authors', 'cote')

    @staticmethod
    def get_authors(obj):
        return "\n".join(p.nom for p in obj.auteur.all())


@admin.register(Game)
class GamesAdmin(VersionAdmin):
    list_display = (
        'nom', 'proprietaire', 'duree', 'nombre_joueurs_min',
        'nombre_joueurs_max', 'comment')
