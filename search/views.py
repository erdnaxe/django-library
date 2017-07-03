# Re2o est  un logiciel d'administration développé initiallement au rezometz. Il
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

# App de recherche pour re2o
# Augustin lemesle, Gabriel Détraz, Goulven Kermarec
# Gplv2
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template.context_processors import csrf
from django.template import Context, RequestContext, loader
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from users.models import User
from search.forms import SearchForm, SearchFormPlus

from med.settings import SEARCH_DISPLAY_PAGE

from media.models import Media, Emprunt

def form(ctx, template, request):
    c = ctx
    c.update(csrf(request))
    return render(request, template, c)

def search_result(search, type, request):
    date_deb = None
    date_fin = None
    states=[]
    aff=[]
    if(type):
        aff = search.cleaned_data['affichage']
        states = search.cleaned_data['filtre']
        date_deb = search.cleaned_data['date_deb']
        date_fin = search.cleaned_data['date_fin']
    date_query = Q()
    if aff==[]:
        aff = ['0','1','2']
    if date_deb != None:
        date_query = date_query & Q(date_emprunt__gte=date_deb)
    if date_fin != None:
        date_query = date_query & Q(date_emprunt__lte=date_fin)
    search = search.cleaned_data['search_field']
    query1 = Q()
    for s in states:
        query1 = query1 | Q(state = s)
    
    connexion = [] 
   
    recherche = {'users_list': None, 'emprunts_list' : None, 'medias_list' : None}

    if request.user.has_perms(('perm',)):
        query = Q(user__pseudo__icontains = search) | Q(user__name__icontains = search) | Q(user__surname__icontains = search)
    else:
        query = (Q(user__pseudo__icontains = search) | Q(user__name__icontains = search) | Q(user__surname__icontains = search)) & Q(user = request.user)


    for i in aff:
        if i == '0':
            query_user_list = Q(pseudo__icontains = search) | Q(name__icontains = search) | Q(surname__icontains = search) & query1
            if request.user.has_perms(('perm',)):
                recherche['users_list'] = User.objects.filter(query_user_list).order_by('state', 'surname')
            else :
                recherche['users_list'] = User.objects.filter(query_user_list & Q(id=request.user.id)).order_by('state', 'surname')
        if i == '1':
            recherche['emprunts_list'] = Emprunt.objects.filter(query & date_query).order_by('date_emprunt').reverse()
        if i == '2':
            recherche['medias_list'] = Media.objects.filter(Q(auteur__nom__icontains = search) | Q(titre__icontains = search))

    for r in recherche:
        if recherche[r] != None:
            recherche[r] = recherche[r][:SEARCH_DISPLAY_PAGE]

    recherche.update({'max_result': SEARCH_DISPLAY_PAGE})

    return recherche

@login_required
def search(request):
    search = SearchForm(request.POST or None)
    if search.is_valid():
        return form(search_result(search, False, request), 'search/index.html',request)
    return form({'searchform' : search}, 'search/search.html', request)

@login_required
def searchp(request):
    search = SearchFormPlus(request.POST or None)
    if search.is_valid():
        return form(search_result(search, True, request), 'search/index.html',request)
    return form({'searchform' : search}, 'search/search.html', request)

