from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.template.context_processors import csrf
from django.utils.translation import gettext_lazy as _

from med.settings import SEARCH_DISPLAY_PAGE
from media.models import Media, Game, BorrowedMedia
from search.forms import SearchForm, AdvancedSearchForm
from users.models import User


def form(ctx, template, request):
    c = ctx
    c.update(csrf(request))
    return render(request, template, c)


def search_result(search_form, type, request):
    date_deb = None
    date_fin = None
    states = []
    aff = []
    if type:
        aff = search_form.cleaned_data['affichage']
        states = search_form.cleaned_data['filtre']
        date_deb = search_form.cleaned_data['date_deb']
        date_fin = search_form.cleaned_data['date_fin']
    date_query = Q()
    if not aff:
        aff = ['0', '1', '2', '3']
    if date_deb is not None:
        date_query = date_query & Q(date_emprunt__gte=date_deb)
    if date_fin is not None:
        date_query = date_query & Q(date_emprunt__lte=date_fin)
    search = search_form.cleaned_data['search_field']
    query1 = Q()
    for s in states:
        query1 = query1 | Q(state=s)

    recherche = {'users_list': None, 'emprunts_list': None, 'medias_list': None,
                 'jeux_list': None}

    if request.user.has_perms(('perm',)):
        query = Q(user__pseudo__icontains=search) | Q(
            user__name__icontains=search) | Q(user__surname__icontains=search)
    else:
        query = (Q(user__pseudo__icontains=search) | Q(
            user__name__icontains=search) | Q(
            user__surname__icontains=search)) & Q(user=request.user)

    for i in aff:
        if i == '0':
            query_user_list = Q(pseudo__icontains=search) | Q(
                name__icontains=search) | Q(surname__icontains=search) & query1
            if request.user.has_perms(('perm',)):
                recherche['users_list'] = User.objects.filter(
                    query_user_list).order_by('state', 'surname')
            else:
                recherche['users_list'] = User.objects.filter(
                    query_user_list & Q(id=request.user.id)).order_by('state',
                                                                      'surname')
        if i == '1':
            recherche['emprunts_list'] = BorrowedMedia.objects.filter(
                query & date_query).order_by('date_emprunt').reverse()
        if i == '2':
            recherche['medias_list'] = Media.objects.filter(
                Q(auteur__nom__icontains=search) | Q(titre__icontains=search))
        if i == '3':
            recherche['jeux_list'] = Game.objects.filter(
                Q(nom__icontains=search) | Q(
                    proprietaire__pseudo__icontains=search) | Q(
                    proprietaire__name__icontains=search) | Q(
                    proprietaire__surname__icontains=search))

    for r in recherche:
        if recherche[r] is not None:
            recherche[r] = recherche[r][:SEARCH_DISPLAY_PAGE]

    recherche.update({'max_result': SEARCH_DISPLAY_PAGE})

    return recherche


@login_required
def search(request):
    search_form = SearchForm(request.POST or None)
    if search_form.is_valid():
        return form(search_result(search_form, False, request),
                    'search/index.html', request)
    return form({'title': _('Search'), 'form': search_form},
                'search/form.html', request)


@login_required
def advanced_search(request):
    search_form = AdvancedSearchForm(request.POST or None)
    if search_form.is_valid():
        return form(search_result(search_form, True, request),
                    'search/index.html', request)
    return form({'title': _('Advanced search'), 'form': search_form},
                'search/form.html', request)
