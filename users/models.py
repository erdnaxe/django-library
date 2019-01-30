from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from med.settings import MAX_EMPRUNT


class User(AbstractUser):
    phone = models.CharField(
        _('phone'),
        max_length=15,
        null=True,
        blank=True,
    )
    max_borrowed = models.IntegerField(
        _('maximum simultaneous borrowed books'),
        default=MAX_EMPRUNT,
    )
    comment = models.CharField(
        _('comment'),
        max_length=255,
        blank=True,
    )

    # Require a valid name
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    @property
    def is_adherent(self):
        return self in Membership.objects.all().order_by(
            '-start_at').first().members.all()


class Key(models.Model):
    name = models.CharField(_('name'), max_length=255, unique=True)
    owner = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name=_('owner'),
    )
    comment = models.CharField(
        _('comment'),
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = _('key')
        verbose_name_plural = _('keys')


class Membership(models.Model):
    start_at = models.IntegerField(_('start at'), unique=True)
    end_at = models.IntegerField(_('end at'), unique=True)
    members = models.ManyToManyField(
        'User',
        blank=True,
        verbose_name=_('members'),
    )

    class Meta:
        ordering = ['-start_at']
        verbose_name = _('membership')
        verbose_name_plural = _('memberships')
