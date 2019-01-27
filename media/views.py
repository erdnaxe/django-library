from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.utils import timezone
from django_tables2 import SingleTableView
from reversion import revisions as reversion

from med.settings import PAGINATION_NUMBER
from users.models import User
from .forms import EmpruntForm, EditEmpruntForm
from .models import Author, Media, Game, BorrowedMedia
from .tables import BorrowedMediaTable, AuthorTable, MediaTable, GamesTable


class Index(PermissionRequiredMixin, SingleTableView):
    """Parent class to all index pages"""
    paginate_by = PAGINATION_NUMBER
    template_name = 'media/index.html'
    model = Game

    def get_permission_required(self):
        return self.model._meta.model_name + '.view',

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = str(self.model._meta.verbose_name)
        context['name_plural'] = str(self.model._meta.verbose_name_plural)
        return context


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
    emprunts_en_cours = BorrowedMedia.objects.filter(date_rendu=None,
                                                     user=user).count()
    if emprunts_en_cours >= user.maxemprunt:
        messages.error(request,
                       "Maximum d'emprunts atteint"
                       "de l'user %s" % user.maxemprunt)
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
        emprunt_instance = BorrowedMedia.objects.get(pk=pk)
    except BorrowedMedia.DoesNotExist:
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
        emprunt_instance = BorrowedMedia.objects.get(pk=pk)
    except BorrowedMedia.DoesNotExist:
        messages.error(request, u"Entrée inexistante")
        return redirect("/media/index_emprunts/")
    with transaction.atomic(), reversion.create_revision():
        emprunt_instance.permanencier_rendu = request.user
        emprunt_instance.date_rendu = timezone.now()
        emprunt_instance.save()
        reversion.set_user(request.user)
        messages.success(request, "Retour enregistré")
    return redirect("/media/index_emprunts/")


class MyBorrowedMediaIndex(PermissionRequiredMixin, SingleTableView):
    """Special list with only user's media"""
    paginate_by = PAGINATION_NUMBER
    template_name = 'media/index.html'
    model = BorrowedMedia
    table_class = BorrowedMediaTable
    permission_required = 'emprunt.my_view'

    def get_queryset(self):
        """Filter here"""
        return BorrowedMedia.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        m = self.model._meta
        context['name'] = str(m.verbose_name)
        context['name_plural'] = str(m.verbose_name_plural)
        return context


class AuthorsIndex(Index):
    model = Author
    table_class = AuthorTable


class MediaIndex(Index):
    model = Media
    table_class = MediaTable


class GamesIndex(Index):
    model = Game
    table_class = GamesTable
