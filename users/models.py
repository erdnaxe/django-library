from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from med.settings import MAX_EMPRUNT


class User(AbstractUser):
    phone = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name=_('phone'),
    )
    address = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('address'),
    )
    max_borrowed = models.IntegerField(
        default=MAX_EMPRUNT,
        verbose_name=_('maximum simultaneous borrowed books'),
    )
    state = models.IntegerField(
        choices=(
            (0, 'STATE_ACTIVE'),
            (1, 'STATE_DISABLED'),
            (2, 'STATE_ARCHIVE'),
        ),
        default=0,
        verbose_name=_('state'),
    )
    comment = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('comment'),
    )

    # Require a valid name
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    @property
    def is_adherent(self):
        return self in Adhesion.objects.all().order_by(
            'start_at').reverse().first().adherent.all()


class Clef(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('name'),
    )
    owner = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name=_('owner'),
    )
    comment = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('comment'),
    )


class Adhesion(models.Model):
    start_at = models.IntegerField(
        unique=True,
        verbose_name=_('start at'),
    )
    end_at = models.IntegerField(
        unique=True,
        verbose_name=_('end at'),
    )
    member = models.ManyToManyField(
        'User',
        blank=True,
        verbose_name=_('member'),
    )
