from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import DeleteView
from django_tables2 import SingleTableView
from reversion import revisions as reversion
from reversion.models import Version
from reversion.views import RevisionMixin

from med.settings import PAGINATION_NUMBER
from users.models import User
from .forms import AuteurForm, MediaForm, JeuForm, EmpruntForm, EditEmpruntForm
from .models import Auteur, Media, Jeu, Emprunt
from .tables import AuthorTable, MediaTable, GamesTable


def form(ctx, template, request):
    c = ctx
    c.update(csrf(request))
    return render(request, template, c)


@login_required
@permission_required('perm')
def add_auteur(request):
    auteur = AuteurForm(request.POST or None)
    if auteur.is_valid():
        with transaction.atomic(), reversion.create_revision():
            auteur.save()
            reversion.set_user(request.user)
            reversion.set_comment("Création")
        messages.success(request, "L'auteur a été ajouté")
        return redirect("/media/index_auteurs/")
    return form({"title": "Création d'un auteur", "form": auteur},
                "media/form.html", request)


@login_required
@permission_required('perm')
def edit_auteur(request, pk):
    try:
        auteur_instance = Auteur.objects.get(pk=pk)
    except Auteur.DoesNotExist:
        messages.error(request, u"Entrée inexistante")
        return redirect("/media/index_auteurs/")
    auteur = AuteurForm(request.POST or None, instance=auteur_instance)
    if auteur.is_valid():
        with transaction.atomic(), reversion.create_revision():
            auteur.save()
            reversion.set_user(request.user)
            reversion.set_comment("Champs modifié(s) : %s" % ', '.join(
                field for field in auteur.changed_data))
        messages.success(request, "Auteur modifié")
        return redirect("/media/index_auteurs/")
    return form({"title": "Modification d'un auteur", "form": auteur},
                "media/form.html", request)


@login_required
@permission_required('perm')
def add_media(request):
    media = MediaForm(request.POST or None)
    if media.is_valid():
        with transaction.atomic(), reversion.create_revision():
            media.save()
            reversion.set_user(request.user)
            reversion.set_comment("Création")
        messages.success(request, "Le media a été ajouté")
        return redirect("/media/index_medias/")
    return form({"title": "Ajout d'un média", "form": media},
                "media/form.html", request)


@login_required
@permission_required('perm')
def edit_media(request, pk):
    try:
        media_instance = Media.objects.get(pk=pk)
    except Media.DoesNotExist:
        messages.error(request, u"Entrée inexistante")
        return redirect("/media/index_medias/")
    media = MediaForm(request.POST or None, instance=media_instance)
    if media.is_valid():
        with transaction.atomic(), reversion.create_revision():
            media.save()
            reversion.set_user(request.user)
            reversion.set_comment("Champs modifié(s) : %s" % ', '.join(
                field for field in media.changed_data))
        messages.success(request, "Media modifié")
        return redirect("/media/index_medias/")
    return form({"title": "Modification d'un média", "form": media},
                "media/form.html", request)


@login_required
@permission_required('perm')
def add_jeu(request):
    jeu = JeuForm(request.POST or None)
    if jeu.is_valid():
        with transaction.atomic(), reversion.create_revision():
            jeu.save()
            reversion.set_user(request.user)
            reversion.set_comment("Création")
        messages.success(request, "Le jeu a été ajouté")
        return redirect("/media/index_jeux/")
    return form({"title": "Création d'un jeu", "form": jeu}, "media/form.html",
                request)


@login_required
@permission_required('perm')
def edit_jeu(request, pk):
    try:
        jeu_instance = Jeu.objects.get(pk=pk)
    except Jeu.DoesNotExist:
        messages.error(request, u"Entrée inexistante")
        return redirect("/media/index_jeux/")
    jeu = JeuForm(request.POST or None, instance=jeu_instance)
    if jeu.is_valid():
        with transaction.atomic(), reversion.create_revision():
            jeu.save()
            reversion.set_user(request.user)
            reversion.set_comment("Champs modifié(s) : %s" % ', '.join(
                field for field in jeu.changed_data))
        messages.success(request, "Media modifié")
        return redirect("/media/index_jeux/")
    return form({"title": "Modification d'un jeu", "form": jeu},
                "media/form.html", request)


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
class Delete(RevisionMixin, DeleteView):
    template_name = 'media/delete.html'


class BorrowedMediaDelete(Delete):
    model = Emprunt
    success_url = reverse_lazy('media:index')
    permission_required = 'emprunt.delete'


class AuthorsIndex(Index):
    model = Auteur
    table_class = AuthorTable
    add_link = 'media:add-auteur'
    permission_required = 'auteur.view'


class AuthorsDelete(Delete):
    model = Auteur
    success_url = reverse_lazy('media:index-auteurs')
    permission_required = 'auteur.delete'


class MediaIndex(Index):
    model = Media
    table_class = MediaTable
    add_link = 'media:add-media'
    permission_required = 'media.view'


class MediaDelete(Delete):
    model = Media
    success_url = reverse_lazy('media:index-medias')
    permission_required = 'media.delete'


class GamesIndex(Index):
    model = Jeu
    table_class = GamesTable
    add_link = 'media:add-jeu'
    permission_required = 'jeu.view'


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
