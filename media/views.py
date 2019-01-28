from django.contrib.auth.mixins import PermissionRequiredMixin
from django_tables2 import SingleTableView

from med.settings import PAGINATION_NUMBER
from .models import Author, Media, Game, BorrowedMedia
from .tables import BorrowedMediaTable, AuthorTable, MediaTable, GamesTable


class Index(PermissionRequiredMixin, SingleTableView):
    """Parent class to all index pages"""
    paginate_by = PAGINATION_NUMBER
    template_name = 'media/index.html'
    model = Game

    def get_permission_required(self):
        return self.model._meta.model_name + '.view',

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = str(self.model._meta.verbose_name)
        context['name_plural'] = str(self.model._meta.verbose_name_plural)
        return context


class MyBorrowedMediaIndex(PermissionRequiredMixin, SingleTableView):
    """Special list with only user's media"""
    paginate_by = PAGINATION_NUMBER
    template_name = 'media/index.html'
    model = BorrowedMedia
    table_class = BorrowedMediaTable
    permission_required = 'borrowedmedia.my_view'

    def get_queryset(self):
        """Filter here"""
        return BorrowedMedia.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        m = self.model._meta
        context['name'] = str(m.verbose_name)
        context['name_plural'] = str(m.verbose_name_plural)
        return context


class AuthorsIndex(Index):
    model = Author
    table_class = AuthorTable


class MediaIndex(Index):
    model = Media
    table_class = MediaTable


class GamesIndex(Index):
    model = Game
    table_class = GamesTable
