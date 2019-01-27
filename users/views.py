from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, UpdateView
from reversion import revisions as reversion
from reversion.views import RevisionMixin

from med.settings import PAGINATION_NUMBER
from media.models import Emprunt
from users.forms import InfoForm, BaseInfoForm, StateForm
from users.models import User, Clef, Adhesion


def form(ctx, template, request):
    c = ctx
    c.update(csrf(request))
    return render(request, template, c)


@login_required
@permission_required('bureau')
def new_user(request):
    """ Vue de création d'un nouvel utilisateur, envoie un mail pour le mot de passe"""
    user = BaseInfoForm(request.POST or None)
    if user.is_valid():
        user = user.save(commit=False)
        with transaction.atomic(), reversion.create_revision():
            user.save()
            reversion.set_comment("Création")
        # TODO send email with password init
        messages.success(request,
                         "L'utilisateur %s a été crée, un mail pour l'initialisation du mot de passe a été envoyé" % user.pseudo)
        return redirect("/users/profil/" + str(user.id))
    return form({'userform': user}, 'users/user.html', request)


@login_required
def edit_info(request, userid):
    """ Edite un utilisateur à partir de son id, si l'id est différent de request.user, vérifie la possession du droit admin """
    try:
        user = User.objects.get(pk=userid)
    except User.DoesNotExist:
        messages.error(request, "Utilisateur inexistant")
        return redirect("/users/")
    if not request.user.has_perms(('bureau',)) and user != request.user:
        messages.error(request,
                       "Vous ne pouvez pas modifier un autre user que vous sans droit admin")
        return redirect("/users/profil/" + str(request.user.id))
    if not request.user.has_perms(('bureau',)):
        user = BaseInfoForm(request.POST or None, instance=user)
    else:
        user = InfoForm(request.POST or None, instance=user)
    if user.is_valid():
        with transaction.atomic(), reversion.create_revision():
            user.save()
            reversion.set_user(request.user)
            reversion.set_comment("Champs modifié(s) : %s" % ', '.join(
                field for field in user.changed_data))
        messages.success(request, "L'user a bien été modifié")
        return redirect("/users/profil/" + userid)
    return form({'userform': user}, 'users/user.html', request)


@login_required
@permission_required('bureau')
def state(request, userid):
    """ Changer l'etat actif/desactivé/archivé d'un user, need droit bureau """
    try:
        user = User.objects.get(pk=userid)
    except User.DoesNotExist:
        messages.error(request, "Utilisateur inexistant")
        return redirect("/users/")
    state = StateForm(request.POST or None, instance=user)
    if state.is_valid():
        with transaction.atomic(), reversion.create_revision():
            state.save()
            reversion.set_user(request.user)
            reversion.set_comment("Champs modifié(s) : %s" % ', '.join(
                field for field in state.changed_data))
        messages.success(request, "Etat changé avec succès")
        return redirect("/users/profil/" + userid)
    return form({'userform': state}, 'users/user.html', request)


@login_required
@permission_required('bureau')
def del_clef(request, clefid):
    try:
        clef_instance = Clef.objects.get(pk=clefid)
    except Clef.DoesNotExist:
        messages.error(request, u"Entrée inexistante")
        return redirect("/users/index_clef/")
    if request.method == "POST":
        with transaction.atomic(), reversion.create_revision():
            clef_instance.delete()
            reversion.set_user(request.user)
            messages.success(request, "La clef a été détruite")
        return redirect("/users/index_clef")
    return form({'objet': clef_instance, 'objet_name': 'clef'},
                'users/delete.html', request)


def index_clef(request):
    clef_list = Clef.objects.all().order_by('nom')
    return render(request, 'users/index_clef.html', {'clef_list': clef_list})


@login_required
@permission_required('bureau')
def del_adhesion(request, adhesionid):
    try:
        adhesion_instance = Adhesion.objects.get(pk=adhesionid)
    except Adhesion.DoesNotExist:
        messages.error(request, u"Entrée inexistante")
        return redirect("/users/index_adhesion/")
    if request.method == "POST":
        with transaction.atomic(), reversion.create_revision():
            adhesion_instance.delete()
            reversion.set_user(request.user)
            messages.success(request, "La adhesion a été détruit")
        return redirect("/users/index_adhesion")
    return form({'objet': adhesion_instance, 'objet_name': 'adhesion'},
                'users/delete.html', request)


@login_required
def index_adhesion(request):
    adhesion_list = Adhesion.objects.all()
    return render(request, 'users/index_adhesion.html',
                  {'adhesion_list': adhesion_list})


@login_required
@permission_required('perm')
def index(request):
    """ Affiche l'ensemble des users, need droit admin """
    users_list = User.objects.order_by('state', 'name')
    paginator = Paginator(users_list, PAGINATION_NUMBER)
    page = request.GET.get('page')
    try:
        users_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users_list = paginator.page(paginator.num_pages)
    return render(request, 'users/index.html', {'users_list': users_list})


@login_required
@permission_required('perm')
def index_ajour(request):
    """ Affiche l'ensemble des users, need droit admin """
    users_list = Adhesion.objects.all().order_by(
        'annee_debut').reverse().first().adherent.all().order_by('name')
    paginator = Paginator(users_list, PAGINATION_NUMBER)
    page = request.GET.get('page')
    try:
        users_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users_list = paginator.page(paginator.num_pages)
    return render(request, 'users/index.html', {'users_list': users_list})


@login_required
def mon_profil(request):
    return redirect("/users/profil/" + str(request.user.id))


@login_required
def profil(request, userid):
    try:
        users = User.objects.get(pk=userid)
    except User.DoesNotExist:
        messages.error(request, "Utilisateur inexistant")
        return redirect("/users/")
    if not request.user.has_perms(('perm',)) and users != request.user:
        messages.error(request,
                       "Vous ne pouvez pas afficher un autre user que vous sans droit perm")
        return redirect("/users/profil/" + str(request.user.id))
    emprunts_list = Emprunt.objects.filter(user=users)
    # list_droits = Right.objects.filter(user=users)
    return render(
        request,
        'users/profil.html',
        {
            'user': users,
            'emprunts_list': emprunts_list,
            # 'list_droits': list_droits,
        }
    )


@login_required
@permission_required('bureau')
def adherer(request, userid):
    try:
        users = User.objects.get(pk=userid)
    except User.DoesNotExist:
        messages.error(request, "Utilisateur inexistant")
        return redirect("/users/")
    adh_annee = Adhesion.objects.all().order_by('annee_debut').reverse().first()
    with transaction.atomic(), reversion.create_revision():
        reversion.set_user(request.user)
        adh_annee.adherent.add(users)
        adh_annee.save()
        reversion.set_comment("Adhesion de %s" % users)
    messages.success(request, "Adhesion effectuee")
    return redirect("/users/profil/" + userid)


class Create(PermissionRequiredMixin, RevisionMixin, SuccessMessageMixin,
             CreateView):
    template_name = 'users/form.html'
    success_message = _('Object successfully created')
    permission_required = 'clef.add'
    fields = '__all__'

    def get_form(self, form_class=None):
        creation_form = super().get_form(form_class)
        creation_form.helper = FormHelper()
        creation_form.helper.add_input(
            Submit('submit', _('Create'), css_class='btn-success'))
        return creation_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Creation')
        return context


class Update(PermissionRequiredMixin, RevisionMixin, SuccessMessageMixin,
             UpdateView):
    """Parent class to all object creation"""
    template_name = 'media/form.html'
    success_message = _('Object successfully edited')

    def get_form(self, form_class=None):
        creation_form = super().get_form(form_class)
        creation_form.helper = FormHelper()
        creation_form.helper.add_input(
            Submit('submit', _('Edit'), css_class='btn-primary'))
        return creation_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Edition')
        return context


class KeyCreate(Create):
    model = Clef
    success_url = reverse_lazy('users:index-clef')
    permission_required = 'clef.add'


class KeyUpdate(Update):
    model = Clef
    success_url = reverse_lazy('media:index-clef')
    permission_required = 'clef.edit'


class MembershipCreate(Create):
    model = Adhesion
    success_url = reverse_lazy('users:index-adhesion')
    permission_required = 'adhesion.add'


class MembershipUpdate(Update):
    model = Adhesion
    success_url = reverse_lazy('media:index-adhesion')
    permission_required = 'adhesion.edit'
