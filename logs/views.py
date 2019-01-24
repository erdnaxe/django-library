from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from reversion.models import Revision

from med.settings import PAGINATION_NUMBER as pagination_number
from users.models import User


def form(ctx, template, request):
    c = ctx
    c.update(csrf(request))
    return render(request, template, c)


@login_required
@permission_required('perm')
def index(request):
    revisions = Revision.objects.all().order_by(
        'date_created').reverse().select_related('user').prefetch_related(
        'version_set__object')
    paginator = Paginator(revisions, pagination_number)
    page = request.GET.get('page')
    try:
        revisions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        revisions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        revisions = paginator.page(paginator.num_pages)
    return render(request, 'logs/index.html', {'revisions_list': revisions})


@login_required
@permission_required('bureau')
def revert_action(request, revision_id):
    """ Annule l'action en question """
    try:
        revision = Revision.objects.get(id=revision_id)
    except Revision.DoesNotExist:
        messages.error(request, u"Revision inexistante")
    if request.method == "POST":
        revision.revert()
        messages.success(request, "L'action a été supprimée")
        return redirect("/logs/")
    return form({'objet': revision, 'objet_name': revision.__class__.__name__},
                'logs/delete.html', request)


@login_required
@permission_required('perm')
def stats_actions(request):
    stats = {
        'Utilisateur': {
            'Action': User.objects.annotate(num=Count('revision')).order_by(
                '-num')[:40],
        },
    }
    return render(request, 'logs/stats_users.html', {'stats_list': stats})
