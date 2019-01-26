from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Auteur(models.Model):
    nom = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('name'),
    )

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['-nom']
        permissions = (
            ("add", "Can add an author"),
            ("change", "Can edit an author"),
            ("delete", "Can delete an author"),
            ("view", "Can view an author"),
        )
        verbose_name = _('author')
        verbose_name_plural = _('authors')


class Media(models.Model):
    titre = models.CharField(
        max_length=255,
        verbose_name=_('title'),
    )
    cote = models.CharField(
        max_length=31,
        verbose_name=_('side title'),
    )
    auteur = models.ManyToManyField(
        'Auteur',
        verbose_name=_('author'),
    )

    def __str__(self):
        return str(self.titre) + ' - ' + str(self.auteur.all().first())

    class Meta:
        ordering = ['-titre']
        permissions = (
            ("add", "Can add a media"),
            ("change", "Can edit a media"),
            ("delete", "Can delete a media"),
            ("view", "Can view a media"),
        )
        verbose_name = _('media')
        verbose_name_plural = _('media')


class Emprunt(models.Model):
    media = models.ForeignKey(
        'Media',
        on_delete=models.PROTECT,
        verbose_name=_('media'),
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        verbose_name=_('borrower'),
    )
    date_emprunt = models.DateTimeField(
        help_text='%d/%m/%y %H:%M:%S',
        verbose_name=_('borrowed at'),
    )
    date_rendu = models.DateTimeField(
        help_text='%d/%m/%y %H:%M:%S',
        blank=True,
        null=True,
        verbose_name=_('given back at'),
    )
    permanencier_emprunt = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='user_permanencier_emprunt',
        verbose_name=_('borrowed with permanent'),
    )
    permanencier_rendu = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='user_permanencier_rendu',
        blank=True,
        null=True,
        verbose_name=_('given back with permanent'),
    )

    def __str__(self):
        return str(self.media) + str(self.user)

    class Meta:
        ordering = ['-date_emprunt']
        permissions = (
            ("add", "Can add a borrowed media"),
            ("change", "Can edit a borrowed media"),
            ("delete", "Can delete a borrowed media"),
            ("my_view", "Can view his borrowed media"),
            ("view", "Can view all borrowed media"),
        )
        verbose_name = _('borrowed media')
        verbose_name_plural = _('borrowed media')


class Jeu(models.Model):
    DUREE = (
        ('-1h', '-1h'),
        ('1-2h', '1-2h'),
        ('2-3h', '2-3h'),
        ('3-4h', '3-4h'),
        ('4h+', '4h+'),
    )

    nom = models.CharField(
        max_length=255,
        verbose_name=_('name'),
    )
    proprietaire = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        verbose_name=_('owner'),
    )
    duree = models.CharField(
        choices=DUREE,
        max_length=255,
        verbose_name=_('length'),
    )
    nombre_joueurs_min = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name=_('minimum number of players'),
    )
    nombre_joueurs_max = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name=_('maximum number of players'),
    )
    comment = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('comment'),
    )

    def __str__(self):
        return str(self.nom)

    class Meta:
        ordering = ['-nom']
        permissions = (
            ("add", "Can add a game"),
            ("change", "Can edit a game"),
            ("delete", "Can delete a game"),
            ("view", "Can view a game"),
        )
        verbose_name = _('game')
        verbose_name_plural = _('games')
