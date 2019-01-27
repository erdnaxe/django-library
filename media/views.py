from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_tables2 import SingleTableView
from reversion import revisions as reversion
from reversion.views import RevisionMixin

from med.settings import PAGINATION_NUMBER
from users.models import User
from .forms import EmpruntForm, EditEmpruntForm
from .models import Author, Media, Game, Emprunt
from .tables import BorrowedMediaTable, AuthorTable, MediaTable, GamesTable


class Index(PermissionRequiredMixin, SingleTableView):
    """Parent class to all index pages"""
    paginate_by = PAGINATION_NUMBER
    template_name = 'media/index.html'
    model = Game
    add_link = False

    def get_permission_required(self):
        return self.model._meta.model_name + '.view',

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        m = self.model._meta
        context['name'] = str(m.verbose_name)
        context['title'] = 'Index des ' + str(m.verbose_name_plural)
        if self.add_link and self.request.user.has_perms(m.model_name + '.add'):
            context['add_link'] = reverse('media:' + m.model_name + '-add')
        return context


class Create(PermissionRequiredMixin, RevisionMixin, SuccessMessageMixin,
             CreateView):
    """Parent class to all object creation"""
    template_name = 'media/form.html'
    success_message = _('Object successfully created')
    fields = '__all__'
    model = Game

    def get_permission_required(self):
        return self.model._meta.model_name + '.add',

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
    fields = '__all__'
    model = Game

    def get_permission_required(self):
        return self.model._meta.model_name + '.edit',

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


class Delete(PermissionRequiredMixin, RevisionMixin, SuccessMessageMixin,
             DeleteView):
    """Parent class to all object deletion"""
    template_name = 'media/delete.html'
    success_message = _('Object successfully deleted')
    model = Game

    def get_permission_required(self):
        return self.model._meta.model_name + '.delete',


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


class AllBorrowedMediaIndex(Index):
    model = Emprunt
    table_class = BorrowedMediaTable


# TODO : filter queryset Emprunt.objects.filter(user=request.user)
class MyBorrowedMediaIndex(PermissionRequiredMixin, SingleTableView):
    """Special list with only user's media"""
    paginate_by = PAGINATION_NUMBER
    template_name = 'media/index.html'
    model = Emprunt
    table_class = BorrowedMediaTable
    permission_required = 'emprunt.my_view'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        m = self.model._meta
        context['name'] = str(m.verbose_name)
        context['title'] = 'Index de mes ' + str(m.verbose_name_plural)
        return context


class BorrowedMediaDelete(Delete):
    model = Emprunt
    success_url = reverse_lazy('media:my-borrowed-index')


class AuthorsIndex(Index):
    model = Author
    table_class = AuthorTable
    add_link = True


class AuthorsCreate(Create):
    model = Author
    success_url = reverse_lazy('media:author-index')


class AuthorsUpdate(Update):
    model = Author
    success_url = reverse_lazy('media:author-index')


class AuthorsDelete(Delete):
    model = Author
    success_url = reverse_lazy('media:author-index')


class MediaIndex(Index):
    model = Media
    table_class = MediaTable
    add_link = True


class MediaCreate(Create):
    model = Media
    success_url = reverse_lazy('media:media-index')


class MediaUpdate(Update):
    model = Media
    success_url = reverse_lazy('media:media-index')


class MediaDelete(Delete):
    model = Media
    success_url = reverse_lazy('media:media-index')


class GamesIndex(Index):
    model = Game
    table_class = GamesTable
    add_link = True


class GamesCreate(Create):
    model = Game
    success_url = reverse_lazy('media:game-index')


class GamesUpdate(Update):
    model = Game
    success_url = reverse_lazy('media:game-index')


class GamesDelete(Delete):
    model = Game
    success_url = reverse_lazy('media:game-index')
