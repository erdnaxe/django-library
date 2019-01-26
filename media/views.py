from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_tables2 import SingleTableView
from reversion import revisions as reversion
from reversion.models import Version
from reversion.views import RevisionMixin

from med.settings import PAGINATION_NUMBER
from users.models import User
from .forms import EmpruntForm, EditEmpruntForm
from .models import Auteur, Media, Jeu, Emprunt
from .tables import AuthorTable, MediaTable, GamesTable


def form(ctx, template, request):
    c = ctx
    c.update(csrf(request))
    return render(request, template, c)


@login_required
@permission_required('perm')
def add_emprunt(request, userid):
    try:
        user = User.objects.get(pk=userid)
    except User.DoesNotExist:
        messages.error(request, u"Entrée inexistante")
        return redirect("/media/index_emprunts/")
    emprunts_en_cours = Emprunt.objects.filter(date_rendu=None,
                                               user=user).count()
    if emprunts_en_cours >= user.maxemprunt:
        messages.error(request,
                       "Maximum d'emprunts atteint de l'user %s" % user.maxemprunt)
        return redirect("/media/index_emprunts/")
    emprunt = EmpruntForm(request.POST or None)
    if emprunt.is_valid():
        emprunt = emprunt.save(commit=False)
        emprunt.user = user
        emprunt.permanencier_emprunt = request.user
        emprunt.date_emprunt = timezone.now()
        with transaction.atomic(), reversion.create_revision():
            emprunt.save()
            reversion.set_user(request.user)
            reversion.set_comment("Création")
        messages.success(request, "Le emprunt a été ajouté")
        return redirect("/media/index_emprunts/")
    return form({"title": "Ajout d'un emprunt", "form": emprunt},
                "media/form.html", request)


@login_required
@permission_required('perm')
def edit_emprunt(request, pk):
    try:
        emprunt_instance = Emprunt.objects.get(pk=pk)
    except Emprunt.DoesNotExist:
        messages.error(request, u"Entrée inexistante")
        return redirect("/media/index_emprunts/")
    emprunt = EditEmpruntForm(request.POST or None, instance=emprunt_instance)
    if emprunt.is_valid():
        with transaction.atomic(), reversion.create_revision():
            emprunt.save()
            reversion.set_user(request.user)
            reversion.set_comment("Champs modifié(s) : %s" % ', '.join(
                field for field in emprunt.changed_data))
        messages.success(request, "Emprunt modifié")
        return redirect("/media/index_emprunts/")
    return form({"title": "Modification d'un emprunt", "form": emprunt},
                "media/form.html", request)


@login_required
@permission_required('perm')
def retour_emprunt(request, pk):
    try:
        emprunt_instance = Emprunt.objects.get(pk=pk)
    except Emprunt.DoesNotExist:
        messages.error(request, u"Entrée inexistante")
        return redirect("/media/index_emprunts/")
    with transaction.atomic(), reversion.create_revision():
        emprunt_instance.permanencier_rendu = request.user
        emprunt_instance.date_rendu = timezone.now()
        emprunt_instance.save()
        reversion.set_user(request.user)
        messages.success(request, "Retour enregistré")
    return redirect("/media/index_emprunts/")


# TODO PermissionRequiredMixin when permissions work
class Index(SingleTableView):
    """Parent class to all index pages"""
    paginate_by = PAGINATION_NUMBER
    template_name = 'media/index.html'
    # TODO find better defaults
    model = Jeu
    add_link = 'media:add-jeu'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO find a way to have proper plural
        context['name'] = self.model._meta.model_name  # Get model name
        context['title'] = 'Index des ' \
                           + self.model._meta.verbose_name_plural.title()
        context['add_link'] = reverse(self.add_link)
        return context


# TODO PermissionRequiredMixin when permissions work
class Create(RevisionMixin, SuccessMessageMixin, CreateView):
    """Parent class to all object creation"""
    template_name = 'media/form.html'
    success_message = _('Object successfully created')

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


# TODO PermissionRequiredMixin when permissions work
class Update(RevisionMixin, SuccessMessageMixin, UpdateView):
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


# TODO PermissionRequiredMixin when permissions work
class Delete(RevisionMixin, SuccessMessageMixin, DeleteView):
    """Parent class to all object deletion"""
    template_name = 'media/delete.html'
    success_message = _('Object successfully deleted')


class BorrowedMediaDelete(Delete):
    model = Emprunt
    success_url = reverse_lazy('media:index')
    permission_required = 'emprunt.delete'


class AuthorsIndex(Index):
    model = Auteur
    table_class = AuthorTable
    add_link = 'media:add-auteur'
    permission_required = 'auteur.view'


class AuthorsCreate(Create):
    model = Auteur
    success_url = reverse_lazy('media:index-auteurs')
    permission_required = 'auteur.add'
    fields = ('nom',)


class AuthorsUpdate(Update):
    model = Auteur
    success_url = reverse_lazy('media:index-auteurs')
    permission_required = 'auteur.edit'
    fields = ('nom',)


class AuthorsDelete(Delete):
    model = Auteur
    success_url = reverse_lazy('media:index-auteurs')
    permission_required = 'auteur.delete'


class MediaIndex(Index):
    model = Media
    table_class = MediaTable
    add_link = 'media:add-media'
    permission_required = 'media.view'


class MediaCreate(Create):
    model = Media
    success_url = reverse_lazy('media:index-medias')
    permission_required = 'media.add'
    fields = ('titre', 'auteur', 'cote')


class MediaUpdate(Update):
    model = Media
    success_url = reverse_lazy('media:index-medias')
    permission_required = 'media.edit'
    fields = ('titre', 'auteur', 'cote')


class MediaDelete(Delete):
    model = Media
    success_url = reverse_lazy('media:index-medias')
    permission_required = 'media.delete'


class GamesIndex(Index):
    model = Jeu
    table_class = GamesTable
    add_link = 'media:add-jeu'
    permission_required = 'jeu.view'


class GamesCreate(Create):
    model = Jeu
    success_url = reverse_lazy('media:index-jeux')
    permission_required = 'jeu.add'
    fields = ('nom', 'proprietaire', 'duree', 'nombre_joueurs_min',
              'nombre_joueurs_max', 'comment')


class GamesUpdate(Update):
    model = Jeu
    success_url = reverse_lazy('media:index-jeux')
    permission_required = 'jeu.edit'
    fields = ('nom', 'proprietaire', 'duree', 'nombre_joueurs_min',
              'nombre_joueurs_max', 'comment')


class GamesDelete(Delete):
    model = Jeu
    success_url = reverse_lazy('media:index-jeux')
    permission_required = 'jeu.delete'


@login_required
def index(request):
    if request.user.has_perms(['perm']):
        emprunts_list = Emprunt.objects.all()
    else:
        emprunts_list = Emprunt.objects.filter(user=request.user)
    paginator = Paginator(emprunts_list.order_by('date_emprunt').reverse(),
                          PAGINATION_NUMBER)
    page = request.GET.get('page')
    try:
        emprunts_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        emprunts_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        emprunts_list = paginator.page(paginator.num_pages)
    return render(request, 'media/index_emprunts.html',
                  {'emprunts_list': emprunts_list})


@login_required
def history(request, object, pk):
    if object == 'auteur':
        try:
            object_instance = Auteur.objects.get(pk=pk)
        except Auteur.DoesNotExist:
            messages.error(request, "Auteur inexistant")
            return redirect("/media/index_auteurs")
    elif object == 'media':
        try:
            object_instance = Media.objects.get(pk=pk)
        except Media.DoesNotExist:
            messages.error(request, "Media inexistant")
            return redirect("/media/index_medias")
    elif object == 'emprunt':
        try:
            object_instance = Emprunt.objects.get(pk=pk)
        except Emprunt.DoesNotExist:
            messages.error(request, "Emprunt inexistant")
            return redirect("/media/index_emprunts")
    elif object == 'jeu':
        try:
            object_instance = Jeu.objects.get(pk=pk)
        except Jeu.DoesNotExist:
            messages.error(request, "Jeu inexistant")
            return redirect("/media/index_jeux")
    reversions = Version.objects.get_for_object(object_instance)
    paginator = Paginator(reversions, PAGINATION_NUMBER)
    page = request.GET.get('page')
    try:
        reversions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        reversions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        reversions = paginator.page(paginator.num_pages)
    return render(request, 'med/history.html',
                  {'reversions': reversions, 'object': object_instance})
