import django_tables2 as tables

from .models import BorrowedMedia, Author, Media, Game


class BaseTable(tables.Table):
    class Meta:
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-hover'}


class BorrowedMediaTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = BorrowedMedia
        fields = ('media.title', 'media.author', 'user', 'borrowed_at',
                  'borrowed_with_permanent', 'given_back_at',
                  'given_back_with_permanent')


class AuthorTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = Author
        fields = ('name',)


class MediaTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = Media
        fields = ('title', 'side_title', 'author', 'isbn', 'edition',
                  'publisher', 'published_on')


class GamesTable(BaseTable):
    # TODO: compute volume
    class Meta(BaseTable.Meta):
        model = Game
        fields = ('name', 'type', 'owner', 'length', 'min_players',
                  'max_players', 'last_time_week_game', 'comment')
