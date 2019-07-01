import django_tables2 as tables
from reversion.models import Revision

from users.models import User


class RevisionTable(tables.Table):
    class Meta:
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped'}
        model = Revision
        orderable = False
        fields = ('version_set.all.first.object', 'user', 'date_created',
                  'comment')


class StatsTable(tables.Table):
    class Meta:
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-striped'}
        model = User
        orderable = False
        fields = ('username', 'num')
