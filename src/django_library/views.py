from django.contrib.auth.mixins import PermissionRequiredMixin
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin, SingleTableView

from med.settings import PAGINATION_NUMBER
from .models import Author, Media, Game, BorrowedMedia
from .tables import BorrowedMediaTable, AuthorTable, MediaTable, GamesTable


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


class AuthorsIndex(PermissionRequiredMixin, SingleTableMixin, FilterView):
    paginate_by = PAGINATION_NUMBER
    template_name = 'media/index.html'
    model = Author
    table_class = AuthorTable
    permission_required = 'author.view'
    filterset_fields = {
        'name': ['contains'],
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = str(self.model._meta.verbose_name)
        context['name_plural'] = str(self.model._meta.verbose_name_plural)
        return context


class MediaIndex(PermissionRequiredMixin, SingleTableMixin, FilterView):
    paginate_by = PAGINATION_NUMBER
    template_name = 'media/index.html'
    model = Media
    table_class = MediaTable
    permission_required = 'media.view'
    filterset_fields = {
        'title': ['contains'],
        'author': ['exact'],
        'isbn': ['contains'],
        'edition': ['contains'],
        'publisher': ['contains'],
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = str(self.model._meta.verbose_name)
        context['name_plural'] = str(self.model._meta.verbose_name_plural)
        return context


class GamesIndex(PermissionRequiredMixin, SingleTableMixin, FilterView):
    paginate_by = PAGINATION_NUMBER
    template_name = 'media/index.html'
    model = Game
    table_class = GamesTable
    permission_required = 'game.view'
    filterset_fields = {
        'name': ['contains'],
        'type': ['exact'],
        'owner': ['exact'],
        'length': ['exact'],
        'min_players': ['lte'],
        'max_players': ['gte'],
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = str(self.model._meta.verbose_name)
        context['name_plural'] = str(self.model._meta.verbose_name_plural)
        return context
