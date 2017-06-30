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

from django.db import models
from django.db.models import Q
from django.forms import ModelForm, Form
from django import forms
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.functional import cached_property


from med.settings import MAX_EMPRUNT, REQ_EXPIRE_HRS
import re, uuid
import datetime

from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import subprocess


class UserManager(BaseUserManager):
    def _create_user(self, pseudo, name, surname, email, password=None, su=False):
        if not pseudo:
            raise ValueError('Users must have an username')

        user = self.model(
            pseudo=pseudo,
            name=name,
            surname=surname,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        if su:
            user.make_admin()
        return user

    def create_user(self, pseudo, name, surname, email, password=None):
        """
        Creates and saves a User with the given pseudo, name, surname, email,
        and password.
        """
        return self._create_user(pseudo, name, surname, email, password, False)

    def create_superuser(self, pseudo, name, surname, email, password):
        """
        Creates and saves a superuser with the given pseudo, name, surname,
        email, and password.
        """
        return self._create_user(pseudo, name, surname, email, password, True)


class User(AbstractBaseUser):
    PRETTY_NAME = "Utilisateurs"
    STATE_ACTIVE = 0
    STATE_DISABLED = 1
    STATE_ARCHIVE = 2
    STATES = (
            (0, 'STATE_ACTIVE'),
            (1, 'STATE_DISABLED'),
            (2, 'STATE_ARCHIVE'),
            )

    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    adresse = models.CharField(max_length=255, null=True, blank=True)
    maxemprunt = models.IntegerField(default=MAX_EMPRUNT, help_text="Maximum d'emprunts autorisés") 
    state = models.IntegerField(choices=STATES, default=STATE_ACTIVE)
    pseudo = models.CharField(max_length=32, unique=True, help_text="Doit contenir uniquement des lettres, chiffres, ou tirets. ")
    comment = models.CharField(help_text="Commentaire, promo", max_length=255, blank=True)
    registered = models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = 'pseudo'
    REQUIRED_FIELDS = ['name', 'surname', 'email']

    objects = UserManager()

    @property
    def is_active(self):
        return self.state == self.STATE_ACTIVE

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_admin(self):
        try:
            Right.objects.get(user=self, right__listright='admin')
        except Right.DoesNotExist:
            return False
        return True

    @is_admin.setter
    def is_admin(self, value):
        if value and not self.is_admin:
            self.make_admin()
        elif not value and self.is_admin:
            self.un_admin()

    def has_perms(self, perms, obj=None):
        for perm in perms:
            try:
                Right.objects.get(user=self, right__listright=perm)
                return True
            except Right.DoesNotExist:
                return False

    def get_full_name(self):
        return '%s %s' % (self.name, self.surname)

    def get_short_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_right(self, right):
        return Right.objects.filter(user=self).filter(right=ListRight.objects.get(listright=right)).exists()

    def has_module_perms(self, app_label):
        # Simplest version again
        return True

    def get_admin_right(self):
        admin, created = ListRight.objects.get_or_create(listright="admin")
        return admin 

    def make_admin(self):
        """ Make User admin """
        user_admin_right = Right(user=self, right=self.get_admin_right())
        user_admin_right.save()
 
    def un_admin(self):
        try:
            user_right = Right.objects.get(user=self,right=self.get_admin_right())
        except Right.DoesNotExist:
            return
        user_right.delete()

    def __str__(self):
        return self.pseudo


class Request(models.Model):
    PASSWD = 'PW'
    EMAIL = 'EM'
    TYPE_CHOICES = (
        (PASSWD, 'Mot de passe'),
        (EMAIL, 'Email'),
    )
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    token = models.CharField(max_length=32)
    user = models.ForeignKey('User', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    expires_at = models.DateTimeField()

    def save(self):
        if not self.expires_at:
            self.expires_at = timezone.now() \
                + datetime.timedelta(hours=REQ_EXPIRE_HRS)
        if not self.token:
            self.token = str(uuid.uuid4()).replace('-', '')  # remove hyphens
        super(Request, self).save()

class Right(models.Model):
    PRETTY_NAME = "Droits affectés à des users"
 
    user = models.ForeignKey('User', on_delete=models.PROTECT)
    right = models.ForeignKey('ListRight', on_delete=models.PROTECT)
 
    class Meta:
        unique_together = ("user", "right")
 
    def __str__(self):
        return str(self.user) + " - " + str(self.right)

class ListRight(models.Model):
    PRETTY_NAME = "Liste des droits existants"

    listright = models.CharField(max_length=255, unique=True)
    details = models.CharField(help_text="Description", max_length=255, blank=True)
 
    def __str__(self):
        return self.listright

class BaseInfoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseInfoForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Prénom'
        self.fields['surname'].label = 'Nom'
        #self.fields['comment'].label = 'Commentaire'

    class Meta:
        model = User
        fields = [
            'name',
            'pseudo',
            'surname',
            'email',
            'telephone',
            'adresse',
        ]

class InfoForm(BaseInfoForm):
    class Meta(BaseInfoForm.Meta):
         fields = [
            'name',
            'pseudo',
            'surname',
            'email',
            'telephone',
            'adresse',
            'maxemprunt',
        ]


class PasswordForm(ModelForm):
    class Meta:
        model = User
        fields = ['password']

class StateForm(ModelForm):
    class Meta:
        model = User
        fields = ['state']

class RightForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RightForm, self).__init__(*args, **kwargs)
        self.fields['right'].label = 'Droit'
        self.fields['right'].empty_label = "Choisir un nouveau droit"

    class Meta:
        model = Right
        fields = ['right']


class DelRightForm(Form):
    rights = forms.ModelMultipleChoiceField(queryset=Right.objects.all(), label="Droits actuels",  widget=forms.CheckboxSelectMultiple)


class ListRightForm(ModelForm):
    class Meta:
        model = ListRight
        fields = ['listright', 'details']

    def __init__(self, *args, **kwargs):
        super(ListRightForm, self).__init__(*args, **kwargs)
        self.fields['listright'].label = 'Nom du droit/groupe'

class NewListRightForm(ListRightForm):
    class Meta(ListRightForm.Meta):
        fields = '__all__'

class DelListRightForm(Form):
    listrights = forms.ModelMultipleChoiceField(queryset=ListRight.objects.all(), label="Droits actuels",  widget=forms.CheckboxSelectMultiple)


