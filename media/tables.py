import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from .models import Emprunt, Author, Media, Game


class BaseTable(tables.Table):
    actions = tables.TemplateColumn(verbose_name=_('Actions'),
                                    template_name='media/action_column.html',
                                    orderable=False)

    class Meta:
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped'}


class BorrowedMediaTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = Emprunt
        fields = ('media', 'user', 'date_emprunt', 'permanencier_emprunt',
                  'date_rendu', 'permanencier_rendu')


class AuthorTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = Author
        fields = ('nom',)


class MediaTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = Media
        fields = ('titre', 'auteur', 'cote')


class GamesTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = Game
        fields = ('nom', 'proprietaire', 'duree', 'nombre_joueurs_min',
                  'nombre_joueurs_max', 'comment')
