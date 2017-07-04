# Re2o est un logiciel d'administration développé initiallement au rezometz. Il
# se veut agnostique au réseau considéré, de manière à être installable en
# quelques clics.
#
# Copyright © 2017  Gabriel Détraz
# Copyright © 2017  Goulven Kermarec
# Copyright © 2017  Augustin Lemesle
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

# App de gestion des statistiques pour re2o
# Gabriel Détraz
# Gplv2
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.template.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import Context, RequestContext, loader
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import ProtectedError
from django.forms import ValidationError
from django.db import transaction
from django.db.models import Count

from reversion.models import Revision
from reversion.models import Version

from users.models import User
from med.settings import PAGINATION_NUMBER as pagination_number

from django.utils import timezone

def form(ctx, template, request):
    c = ctx
    c.update(csrf(request))
    return render(request, template, c)

@login_required
@permission_required('perm')
def index(request):
    revisions = Revision.objects.all().order_by('date_created').reverse().select_related('user').prefetch_related('version_set__object')
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
        messages.error(request, u"Revision inexistante" )
    if request.method == "POST":
        revision.revert()
        messages.success(request, "L'action a été supprimée")
        return redirect("/logs/")
    return form({'objet': revision, 'objet_name': revision.__class__.__name__ }, 'logs/delete.html', request)

@login_required
@permission_required('perm')
def stats_actions(request):
    onglet = request.GET.get('onglet')
    stats = {
    'Utilisateur' : {
    'Action' : User.objects.annotate(num=Count('revision')).order_by('-num')[:40],
    },
    }
    return render(request, 'logs/stats_users.html', {'stats_list': stats})
