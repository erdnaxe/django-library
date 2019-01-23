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

# App de gestion des users pour med
# Goulven Kermarec, Gabriel Détraz, Lemesle Augustin
# Gplv2
from django.shortcuts import get_object_or_404, render, redirect
from django.template.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import Context, RequestContext, loader
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.signals import user_logged_in
from django.db.models import Max, ProtectedError
from django.db import IntegrityError
from django.core.mail import send_mail
from django.utils import timezone
from django.urls import reverse
from django.db import transaction

from reversion.models import Version
from reversion import revisions as reversion
from users.forms import DelListRightForm, NewListRightForm, ListRightForm, RightForm, DelRightForm
from users.forms import InfoForm, BaseInfoForm, StateForm, ClefForm, BaseClefForm, AdhesionForm 
from users.models import User, Request, ListRight, Right, Clef, Adhesion
from users.forms import PassForm, ResetPasswordForm
from users.decorators import user_is_in_campus
from media.models import Emprunt

from med.settings import REQ_EXPIRE_STR, EMAIL_FROM, ASSO_NAME, ASSO_EMAIL, SITE_NAME, PAGINATION_NUMBER


def form(ctx, template, request):
    c = ctx
    c.update(csrf(request))
    return render(request, template, c)

def password_change_action(u_form, user, request, req=False):
    """ Fonction qui effectue le changeemnt de mdp bdd"""
    if u_form.cleaned_data['passwd1'] != u_form.cleaned_data['passwd2']:
        messages.error(request, "Les 2 mots de passe différent")
        return form({'userform': u_form}, 'users/user.html', request)
    user.set_password(u_form.cleaned_data['passwd1'])
    with transaction.atomic(), reversion.create_revision():
        user.save()
        reversion.set_comment("Réinitialisation du mot de passe")
    messages.success(request, "Le mot de passe a changé")
    if req:
        req.delete()
        return redirect("/")
    return redirect("/users/profil/" + str(user.id))

def reset_passwd_mail(req, request):
    """ Prend en argument un request, envoie un mail de réinitialisation de mot de pass """
    t = loader.get_template('users/email_passwd_request')
    c = {
      'name': str(req.user.name) + ' ' + str(req.user.surname),
      'asso': ASSO_NAME,
      'asso_mail': ASSO_EMAIL,
      'site_name': SITE_NAME,
      'url': request.build_absolute_uri(
       reverse('users:process', kwargs={'token': req.token})),
       'expire_in': REQ_EXPIRE_STR,
    }
    send_mail('Votre compte %s' % SITE_NAME, t.render(c),
    EMAIL_FROM, [req.user.email], fail_silently=False)
    return


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
        req = Request()
        req.type = Request.PASSWD
        req.user = user
        req.save()
        reset_passwd_mail(req, request)
        messages.success(request, "L'utilisateur %s a été crée, un mail pour l'initialisation du mot de passe a été envoyé" % user.pseudo)
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
        messages.error(request, "Vous ne pouvez pas modifier un autre user que vous sans droit admin")
        return redirect("/users/profil/" + str(request.user.id))
    if not request.user.has_perms(('bureau',)):
        user = BaseInfoForm(request.POST or None, instance=user)
    else:
        user = InfoForm(request.POST or None, instance=user)
    if user.is_valid():
        with transaction.atomic(), reversion.create_revision():
            user.save()
            reversion.set_user(request.user)
            reversion.set_comment("Champs modifié(s) : %s" % ', '.join(field for field in user.changed_data))
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
            reversion.set_comment("Champs modifié(s) : %s" % ', '.join(field for field in state.changed_data))
        messages.success(request, "Etat changé avec succès")
        return redirect("/users/profil/" + userid)
    return form({'userform': state}, 'users/user.html', request)

@login_required
def password(request, userid):
    """ Reinitialisation d'un mot de passe à partir de l'userid,
    pour self par défaut, pour tous sans droit si droit admin,
    pour tous si droit bureau """
    try:
        user = User.objects.get(pk=userid)
    except User.DoesNotExist:
        messages.error(request, "Utilisateur inexistant")
        return redirect("/users/")
    if not request.user.has_perms(('bureau',)) and user != request.user:
        messages.error(request, "Vous ne pouvez pas modifier un autre user que vous sans droit admin")
        return redirect("/users/profil/" + str(request.user.id))
    u_form = PassForm(request.POST or None)
    if u_form.is_valid():
        return password_change_action(u_form, user, request)
    return form({'userform': u_form}, 'users/user.html', request)

@login_required
@permission_required('bureau')
def add_listright(request):
    """ Ajouter un droit/groupe, nécessite droit bureau.
    Obligation de fournir un gid pour la synchro ldap, unique """
    listright = NewListRightForm(request.POST or None)
    if listright.is_valid():
        with transaction.atomic(), reversion.create_revision():
            listright.save()
            reversion.set_user(request.user)
            reversion.set_comment("Création")
        messages.success(request, "Le droit/groupe a été ajouté")
        return redirect("/users/index_listright/")
    return form({'userform': listright}, 'users/user.html', request)

@login_required
@permission_required('bureau')
def edit_listright(request, listrightid):
    """ Editer un groupe/droit, necessite droit bureau, à partir du listright id """
    try:
        listright_instance = ListRight.objects.get(pk=listrightid)
    except ListRight.DoesNotExist:
        messages.error(request, u"Entrée inexistante" )
        return redirect("/users/")
    listright = ListRightForm(request.POST or None, instance=listright_instance)
    if listright.is_valid():
        with transaction.atomic(), reversion.create_revision():
            listright.save()
            reversion.set_user(request.user)
            reversion.set_comment("Champs modifié(s) : %s" % ', '.join(field for field in listright.changed_data))
        messages.success(request, "Droit modifié")
        return redirect("/users/index_listright/")
    return form({'userform': listright}, 'users/user.html', request)

@login_required
@permission_required('bureau')
def del_listright(request):
    """ Supprimer un ou plusieurs groupe, possible si il est vide, need droit bureau """
    listright = DelListRightForm(request.POST or None)
    if listright.is_valid():
        listright_dels = listright.cleaned_data['listrights']
        for listright_del in listright_dels:
            try:
                with transaction.atomic(), reversion.create_revision():
                    listright_del.delete()
                    reversion.set_comment("Destruction")
                messages.success(request, "Le droit/groupe a été supprimé")
            except ProtectedError:
                messages.error(
                    request,
                    "L'établissement %s est affecté à au moins un user, \
                        vous ne pouvez pas le supprimer" % listright_del)
        return redirect("/users/index_listright/")
    return form({'userform': listright}, 'users/user.html', request)

@login_required
@permission_required('bureau')
def add_right(request, userid):
    """ Ajout d'un droit à un user, need droit bureau """
    try:
        user = User.objects.get(pk=userid)
    except User.DoesNotExist:
        messages.error(request, "Utilisateur inexistant")
        return redirect("/users/")
    right = RightForm(request.POST or None)
    if right.is_valid():
        right = right.save(commit=False)
        right.user = user
        try:
            with transaction.atomic(), reversion.create_revision():
                reversion.set_user(request.user)
                reversion.set_comment("Ajout du droit %s" % right.right)
                right.save()
            messages.success(request, "Droit ajouté")
        except IntegrityError:
            pass
        return redirect("/users/profil/" + userid)
    return form({'userform': right}, 'users/user.html', request)

@login_required
@permission_required('bureau')
def del_right(request):
    """ Supprimer un droit à un user, need droit bureau """
    user_right_list = dict()
    for right in ListRight.objects.all():
        user_right_list[right]= DelRightForm(right, request.POST or None)
    for keys, right_item in user_right_list.items():
        if right_item.is_valid():
            right_del = right_item.cleaned_data['rights']
            with transaction.atomic(), reversion.create_revision():
                reversion.set_user(request.user)
                reversion.set_comment("Retrait des droit %s" % ','.join(str(deleted_right) for deleted_right in right_del))
                right_del.delete()
            messages.success(request, "Droit retiré avec succès")
            return redirect("/users/")
    return form({'userform': user_right_list}, 'users/del_right.html', request)

@login_required
@permission_required('perm')
def index_listright(request):
    """ Affiche l'ensemble des droits , need droit perm """
    listright_list = ListRight.objects.order_by('listright')
    return render(request, 'users/index_listright.html', {'listright_list':listright_list})

@login_required
@permission_required('bureau')
def add_clef(request):
    clef = ClefForm(request.POST or None)
    if clef.is_valid():
        with transaction.atomic(), reversion.create_revision():
            clef.save()
            reversion.set_user(request.user)
            reversion.set_comment("Création")
        messages.success(request, "La clef a été ajouté")
        return redirect("/users/index_clef/")
    return form({'userform': clef}, 'users/user.html', request)

@user_is_in_campus
def edit_clef(request, clefid):
    try:
        clef_instance = Clef.objects.get(pk=clefid)
    except Clef.DoesNotExist:
        messages.error(request, u"Entrée inexistante" )
        return redirect("/users/index_clef/")
    clef = ClefForm(request.POST or None, instance=clef_instance)
    if clef.is_valid():
        with transaction.atomic(), reversion.create_revision():
            clef.save()
            if request.user.is_authenticated:
                reversion.set_user(request.user)
            reversion.set_comment("Champs modifié(s) : %s" % ', '.join(field for field in clef.changed_data))
        messages.success(request, "Clef modifié")
        return redirect("/users/index_clef/")
    return form({'userform': clef}, 'users/user.html', request)

@login_required
@permission_required('bureau')
def del_clef(request, clefid):
    try:
        clef_instance = Clef.objects.get(pk=clefid)
    except Clef.DoesNotExist:
        messages.error(request, u"Entrée inexistante" )
        return redirect("/users/index_clef/")
    if request.method == "POST":
        with transaction.atomic(), reversion.create_revision():
            clef_instance.delete()
            reversion.set_user(request.user)
            messages.success(request, "La clef a été détruite")
        return redirect("/users/index_clef")
    return form({'objet': clef_instance, 'objet_name': 'clef'}, 'users/delete.html', request)

@user_is_in_campus
def index_clef(request):
    clef_list = Clef.objects.all().order_by('nom')
    return render(request, 'users/index_clef.html', {'clef_list':clef_list})

@login_required
@permission_required('bureau')
def add_adhesion(request):
    adhesion = AdhesionForm(request.POST or None)
    if adhesion.is_valid():
        with transaction.atomic(), reversion.create_revision():
            adhesion.save()
            reversion.set_user(request.user)
            reversion.set_comment("Création")
        messages.success(request, "L'adhesion a été ajouté")
        return redirect("/users/index_adhesion/")
    return form({'userform': adhesion}, 'users/user.html', request)

@login_required
@permission_required('bureau')
def edit_adhesion(request, adhesionid):
    try:
        adhesion_instance = Adhesion.objects.get(pk=adhesionid)
    except Adhesion.DoesNotExist:
        messages.error(request, u"Entrée inexistante" )
        return redirect("/users/index_adhesion/")
    adhesion = AdhesionForm(request.POST or None, instance=adhesion_instance)
    if adhesion.is_valid():
        with transaction.atomic(), reversion.create_revision():
            adhesion.save()
            reversion.set_user(request.user)
            reversion.set_comment("Champs modifié(s) : %s" % ', '.join(field for field in adhesion.changed_data))
        messages.success(request, "Adhesion modifiée")
        return redirect("/users/index_adhesion/")
    return form({'userform': adhesion}, 'users/user.html', request)

@login_required
@permission_required('bureau')
def del_adhesion(request, adhesionid):
    try:
        adhesion_instance = Adhesion.objects.get(pk=adhesionid)
    except Adhesion.DoesNotExist:
        messages.error(request, u"Entrée inexistante" )
        return redirect("/users/index_adhesion/")
    if request.method == "POST":
        with transaction.atomic(), reversion.create_revision():
            adhesion_instance.delete()
            reversion.set_user(request.user)
            messages.success(request, "La adhesion a été détruit")
        return redirect("/users/index_adhesion")
    return form({'objet': adhesion_instance, 'objet_name': 'adhesion'}, 'users/delete.html', request)

@login_required
def index_adhesion(request):
    adhesion_list = Adhesion.objects.all()
    return render(request, 'users/index_adhesion.html', {'adhesion_list':adhesion_list})

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
    users_list = Adhesion.objects.all().order_by('annee_debut').reverse().first().adherent.all().order_by('name')
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

@user_is_in_campus
def history(request, object, id):
    """ Affichage de l'historique : (acl, argument)
    user : self, userid"""
    if object == 'clef':
        try:
             object_instance = Clef.objects.get(pk=id)
        except Clef.DoesNotExist:
             messages.error(request, "Utilisateur inexistant")
             return redirect("/users/")
    elif not request.user.is_authenticated:
        messages.error(request, "Permission denied")
        return redirect("/users/")
    if object == 'user':
        try:
             object_instance = User.objects.get(pk=id)
        except User.DoesNotExist:
             messages.error(request, "Utilisateur inexistant")
             return redirect("/users/")
        if not request.user.has_perms(('perm',)) and object_instance != request.user:
             messages.error(request, "Vous ne pouvez pas afficher l'historique d'un autre user que vous sans droit admin")
             return redirect("/users/profil/" + str(request.user.id))
    elif object == 'clef':
        try:
             object_instance = Clef.objects.get(pk=id)
        except Clef.DoesNotExist:
             messages.error(request, "Utilisateur inexistant")
             return redirect("/users/")
    elif object == 'adhesion':
        try:
             object_instance = Adhesion.objects.get(pk=id)
        except Adhesion.DoesNotExist:
             messages.error(request, "Utilisateur inexistant")
             return redirect("/users/")
    elif object == 'listright':
        try:
             object_instance = ListRight.objects.get(pk=id)
        except ListRight.DoesNotExist:
             messages.error(request, "Droit inexistant")
             return redirect("/users/")
    else:
        messages.error(request, "Objet  inconnu")
        return redirect("/users/")
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
        messages.error(request, "Vous ne pouvez pas afficher un autre user que vous sans droit perm")
        return redirect("/users/profil/" + str(request.user.id))
    emprunts_list = Emprunt.objects.filter(user=users)
    list_droits = Right.objects.filter(user=users)
    return render(
        request,
        'users/profil.html',
        {
            'user': users,
            'emprunts_list': emprunts_list,
            'list_droits': list_droits,  
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
 

def reset_password(request):
    userform = ResetPasswordForm(request.POST or None)
    if userform.is_valid():
        try:
            user = User.objects.get(pseudo=userform.cleaned_data['pseudo'],email=userform.cleaned_data['email'])
        except User.DoesNotExist:
            messages.error(request, "Cet utilisateur n'existe pas")
            return form({'userform': userform}, 'users/user.html', request)
        req = Request()
        req.type = Request.PASSWD
        req.user = user
        req.save()
        reset_passwd_mail(req, request)
        messages.success(request, "Un mail pour l'initialisation du mot de passe a été envoyé")
        redirect("/")
    return form({'userform': userform}, 'users/user.html', request)

def process(request, token):
    valid_reqs = Request.objects.filter(expires_at__gt=timezone.now())
    req = get_object_or_404(valid_reqs, token=token)

    if req.type == Request.PASSWD:
        return process_passwd(request, req)
    elif req.type == Request.EMAIL:
        return process_email(request, req=req)
    else:
        messages.error(request, "Entrée incorrecte, contactez un admin")
        redirect("/")

def process_passwd(request, req):
    u_form = PassForm(request.POST or None)
    user = req.user
    if u_form.is_valid():
        return password_change_action(u_form, user, request, req=req)
    return form({'userform': u_form}, 'users/user.html', request)
