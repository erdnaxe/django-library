from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Author, BorrowedMedia, Media, Game


@admin.register(BorrowedMedia)
class BorrowedMediaAdmin(VersionAdmin):
    list_display = ('media', 'user', 'borrowed_at', 'given_back_at',
                    'permanencier_emprunt', 'permanencier_rendu')


@admin.register(Author)
class AuthorAdmin(VersionAdmin):
    list_display = ('name',)


@admin.register(Media)
class MediaAdmin(VersionAdmin):
    list_display = ('title', 'get_authors', 'side_title')

    @staticmethod
    def get_authors(obj):
        return "\n".join(p.name for p in obj.author.all())


@admin.register(Game)
class GamesAdmin(VersionAdmin):
    list_display = ('name', 'owner', 'length', 'min_players', 'max_players',
                    'comment')
