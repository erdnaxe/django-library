from django.db.models import Count
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin, SingleTableView
from reversion.models import Revision

from med.settings import PAGINATION_NUMBER
from users.models import User
from .mixins import SuperUserRequiredMixin
from .tables import RevisionTable, StatsTable


class LogsIndex(SuperUserRequiredMixin, SingleTableMixin, FilterView):
    paginate_by = PAGINATION_NUMBER
    template_name = 'logs/index.html'
    model = Revision
    table_class = RevisionTable
    filterset_fields = ['user']

    def get_queryset(self):
        return Revision.objects.all().order_by(
            'date_created').reverse().select_related('user').prefetch_related(
            'version_set__object')


class StatsIndex(SuperUserRequiredMixin, SingleTableView):
    paginate_by = PAGINATION_NUMBER
    template_name = 'logs/index.html'
    model = User
    table_class = StatsTable

    def get_queryset(self):
        return User.objects.annotate(num=Count('revision')).order_by('-num')
