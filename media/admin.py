from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Author, BorrowedMedia, Media, GameType, Game


@admin.register(BorrowedMedia)
class BorrowedMediaAdmin(VersionAdmin):
    list_display = ('media', 'user', 'borrowed_at', 'given_back_at',
                    'borrowed_with_permanent', 'given_back_with_permanent')


@admin.register(Author)
class AuthorAdmin(VersionAdmin):
    list_display = ('name',)


@admin.register(Media)
class MediaAdmin(VersionAdmin):
    list_display = ('title', 'get_authors', 'side_title')

    @staticmethod
    def get_authors(obj):
        return "\n".join(p.name for p in obj.author.all())


@admin.register(GameType)
class GameTypeAdmin(VersionAdmin):
    list_display = ('name',)


@admin.register(Game)
class GamesAdmin(VersionAdmin):
    list_display = ('name', 'type', 'owner', 'length', 'min_players',
                    'max_players', 'box_length', 'box_width', 'box_depth',
                    'last_time_week_game', 'comment')
