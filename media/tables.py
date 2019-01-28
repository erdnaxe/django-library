import django_tables2 as tables

from .models import BorrowedMedia, Author, Media, Game


class BaseTable(tables.Table):
    class Meta:
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped'}


class BorrowedMediaTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = BorrowedMedia
        fields = ('media', 'user', 'borrowed_at', 'permanencier_emprunt',
                  'given_back_at', 'permanencier_rendu')


class AuthorTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = Author
        fields = ('name',)


class MediaTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = Media
        fields = ('title', 'author', 'side_title')


class GamesTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = Game
        fields = ('name', 'owner', 'length', 'min_players', 'max_players',
                  'comment')
