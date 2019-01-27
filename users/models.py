from django.contrib.auth.models import AbstractUser
from django.db import models

from med.settings import MAX_EMPRUNT


class User(AbstractUser):
    PRETTY_NAME = "Utilisateurs"

    telephone = models.CharField(
        max_length=15,
        null=True,
        blank=True,
    )
    adresse = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    maxemprunt = models.IntegerField(
        default=MAX_EMPRUNT,
        help_text="Maximum d'emprunts autorisés",
    )
    state = models.IntegerField(
        choices=(
            (0, 'STATE_ACTIVE'),
            (1, 'STATE_DISABLED'),
            (2, 'STATE_ARCHIVE'),
        ),
        default=0,
    )
    comment = models.CharField(
        help_text="Commentaire, promo",
        max_length=255,
        blank=True,
    )

    # Require a valid name
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    @property
    def is_adherent(self):
        return self in Adhesion.objects.all().order_by(
            'annee_debut').reverse().first().adherent.all()

    def __str__(self):
        return self.username


class Clef(models.Model):
    nom = models.CharField(
        max_length=255,
        unique=True,
    )

    proprio = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    commentaire = models.CharField(
        max_length=255, null=True, blank=True
    )


class Adhesion(models.Model):
    annee_debut = models.IntegerField(
        unique=True,
    )
    annee_fin = models.IntegerField(
        unique=True,
    )
    adherent = models.ManyToManyField(
        'User',
        blank=True,
    )
