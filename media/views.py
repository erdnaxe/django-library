from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.context_processors import csrf
from django.template import Context, RequestContext, loader
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .forms import AuteurForm, MediaForm, EmpruntForm, EditEmpruntForm
from .models import Auteur, Media, Emprunt
from users.models import User
from django.db import transaction
from reversion import revisions as reversion
from reversion.models import Version

from med.settings import PAGINATION_NUMBER

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
    return form({'mediaform': auteur}, 'media/media.html', request)

@login_required
@permission_required('perm')
def edit_auteur(request, auteurid):
    try:
        auteur_instance = Auteur.objects.get(pk=auteurid)
    except Auteur.DoesNotExist:
        messages.error(request, u"Entrée inexistante" )
        return redirect("/media/index_auteurs/")
    auteur = AuteurForm(request.POST or None, instance=auteur_instance)
    if auteur.is_valid():
        with transaction.atomic(), reversion.create_revision():
            auteur.save()
            reversion.set_user(request.user)
            reversion.set_comment("Champs modifié(s) : %s" % ', '.join(field for field in auteur.changed_data))
        messages.success(request, "Auteur modifié")
        return redirect("/media/index_auteurs/")
    return form({'mediaform': auteur}, 'media/media.html', request)

@login_required
@permission_required('perm')
def del_auteur(request, auteurid):
    try:
        auteur_instance = Auteur.objects.get(pk=auteurid)
    except Auteur.DoesNotExist:
        messages.error(request, u"Entrée inexistante" )
        return redirect("/media/index_auteurs/")
    if request.method == "POST":
        with transaction.atomic(), reversion.create_revision():
            auteur_instance.delete()
            reversion.set_user(request.user)
            messages.success(request, "L'auteur a été détruit")
        return redirect("/media/index_auteurs")
    return form({'objet': auteur_instance, 'objet_name': 'auteur'}, 'media/delete.html', request)


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
    return form({'mediaform': media}, 'media/media.html', request)

@login_required
@permission_required('perm')
def edit_media(request, mediaid):
    try:
        media_instance = Media.objects.get(pk=mediaid)
    except Media.DoesNotExist:
        messages.error(request, u"Entrée inexistante" )
        return redirect("/media/index_medias/")
    media = MediaForm(request.POST or None, instance=media_instance)
    if media.is_valid():
        with transaction.atomic(), reversion.create_revision():
            media.save()
            reversion.set_user(request.user)
            reversion.set_comment("Champs modifié(s) : %s" % ', '.join(field for field in media.changed_data))
        messages.success(request, "Media modifié")
        return redirect("/media/index_medias/")
    return form({'mediaform': media}, 'media/media.html', request)

@login_required
@permission_required('perm')
def del_media(request, mediaid):
    try:
        media_instance = Media.objects.get(pk=mediaid)
    except Media.DoesNotExist:
        messages.error(request, u"Entrée inexistante" )
        return redirect("/media/index_medias/")
    if request.method == "POST":
        with transaction.atomic(), reversion.create_revision():
            media_instance.delete()
            reversion.set_user(request.user)
            messages.success(request, "Le media a été détruit")
        return redirect("/media/index_medias")
    return form({'objet': media_instance, 'objet_name': 'media'}, 'media/delete.html', request)

@login_required
@permission_required('perm')
def add_emprunt(request, userid):
    try:
        user = User.objects.get(pk=userid)
    except User.DoesNotExist:
        messages.error(request, u"Entrée inexistante" )
        return redirect("/media/index_emprunts/")
    emprunts_en_cours = Emprunt.objects.filter(date_rendu=None, user=user).count()
    if emprunts_en_cours >= user.maxemprunt:
        messages.error(request, "Maximum d'emprunts atteint de l'user %s" % user.maxemprunt)
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
    return form({'mediaform': emprunt}, 'media/media.html', request)

@login_required
@permission_required('perm')
def edit_emprunt(request, empruntid):
    try:
        emprunt_instance = Emprunt.objects.get(pk=empruntid)
    except Emprunt.DoesNotExist:
        messages.error(request, u"Entrée inexistante" )
        return redirect("/media/index_emprunts/")
    emprunt = EditEmpruntForm(request.POST or None, instance=emprunt_instance)
    if emprunt.is_valid():
        with transaction.atomic(), reversion.create_revision():
            emprunt.save()
            reversion.set_user(request.user)
            reversion.set_comment("Champs modifié(s) : %s" % ', '.join(field for field in emprunt.changed_data))
        messages.success(request, "Emprunt modifié")
        return redirect("/media/index_emprunts/")
    return form({'mediaform': emprunt}, 'media/media.html', request)

@login_required
@permission_required('bureau')
def retour_emprunt(request, empruntid):
    try:
        emprunt_instance = Emprunt.objects.get(pk=empruntid)
    except Emprunt.DoesNotExist:
        messages.error(request, u"Entrée inexistante" )
        return redirect("/media/index_emprunts/")
    with transaction.atomic(), reversion.create_revision():
        emprunt_instance.permanencier_rendu = request.user
        emprunt_instance.date_rendu = timezone.now()
        emprunt_instance.save()
        reversion.set_user(request.user)
        messages.success(request, "Retour enregistré")
    return redirect("/media/index_emprunts/")

@login_required
@permission_required('bureau')
def del_emprunt(request, empruntid):
    try:
        emprunt_instance = Emprunt.objects.get(pk=empruntid)
    except Emprunt.DoesNotExist:
        messages.error(request, u"Entrée inexistante" )
        return redirect("/media/index_emprunts/")
    if request.method == "POST":
        with transaction.atomic(), reversion.create_revision():
            emprunt_instance.delete()
            reversion.set_user(request.user)
            messages.success(request, "L'emprunt a été détruit")
        return redirect("/media/index_emprunts")
    return form({'objet': emprunt_instance, 'objet_name': 'emprunt'}, 'media/delete.html', request)




@login_required
def index_auteurs(request):
    auteurs_list = Auteur.objects.all()
    paginator = Paginator(auteurs_list, PAGINATION_NUMBER)
    page = request.GET.get('page')
    try:
        auteurs_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        auteurs_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        auteurs_list = paginator.page(paginator.num_pages)
    return render(request, 'media/index_auteurs.html', {'auteurs_list':auteurs_list})

@login_required
def index_medias(request):
    medias_list = Media.objects.all()
    paginator = Paginator(medias_list, PAGINATION_NUMBER)
    page = request.GET.get('page')
    try:
        medias_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        medias_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        medias_list = paginator.page(paginator.num_pages)
    return render(request, 'media/index_medias.html', {'medias_list':medias_list})


@login_required
def index(request):
    if request.user.has_perms(['perm']):
        emprunts_list = Emprunt.objects.all()
    else:
        emprunts_list = Emprunt.objects.filter(user=request.user)
    paginator = Paginator(emprunts_list.order_by('date_emprunt').reverse(), PAGINATION_NUMBER)
    page = request.GET.get('page')
    try:
        emprunts_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        emprunts_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        emprunts_list = paginator.page(paginator.num_pages)
    return render(request, 'media/index_emprunts.html', {'emprunts_list':emprunts_list})


@login_required
def history(request, object, id):
    if object == 'auteur':
        try:
             object_instance = Auteur.objects.get(pk=id)
        except Auteur.DoesNotExist:
             messages.error(request, "Auteur inexistant")
             return redirect("/media/index_auteurs")
    elif object == 'media':
        try:
             object_instance = Media.objects.get(pk=id)
        except Media.DoesNotExist:
             messages.error(request, "Media inexistant")
             return redirect("/media/index_medias")
    elif object == 'emprunt':
        try:
             object_instance = Emprunt.objects.get(pk=id)
        except Emprunt.DoesNotExist:
             messages.error(request, "Emprunt inexistant")
             return redirect("/media/index_emprunts")
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
    return render(request, 'med/history.html', {'reversions': reversions, 'object': object_instance})

