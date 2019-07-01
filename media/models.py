from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .fields import ISBNField


class Author(models.Model):
    name = models.CharField(_('name'), max_length=255, unique=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['name']
        verbose_name = _('author')
        verbose_name_plural = _('authors')


class Media(models.Model):
    title = models.CharField(_('title'), max_length=255)
    side_title = models.CharField(
        _('side title'),
        max_length=31,
        blank=True,
        null=True,
    )
    author = models.ManyToManyField('Author', verbose_name=_('author'))
    isbn = ISBNField(
        _('ISBN'),
        blank=True,
        null=True,
    )
    edition = models.CharField(
        _('edition'),
        max_length=255,
        blank=True,
        null=True,
    )
    binding = models.CharField(
        _('binding'),
        max_length=255,
        blank=True,
        null=True,
    )
    publisher = models.CharField(
        _('publisher'),
        max_length=255,
        blank=True,
        null=True,
    )
    published_on = models.DateField(
        _('published on'),
        blank=True,
        null=True,
    )

    def __str__(self):
        return "Media {} by {}".format(self.title, self.author.all().first())

    class Meta:
        ordering = ['-title']
        verbose_name = _('media')
        verbose_name_plural = _('media')


class BorrowedMedia(models.Model):
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
    borrowed_at = models.DateTimeField(_('borrowed at'))
    given_back_at = models.DateTimeField(
        _('given back at'),
        blank=True,
        null=True,
    )
    borrowed_with_permanent = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='user_borrowed_with_permanent',
        verbose_name=_('borrowed with permanent'),
    )
    given_back_with_permanent = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='user_given_back_with_permanent',
        blank=True,
        null=True,
        verbose_name=_('given back with permanent'),
    )

    def __str__(self):
        return "{} borrowed by {}".format(self.media, self.user)

    class Meta:
        ordering = ['-borrowed_at']
        permissions = (
            ("my_view", "Can view his borrowed media"),
        )
        verbose_name = _('borrowed media')
        verbose_name_plural = _('borrowed medias')


class GameType(models.Model):
    name = models.CharField(_('name'), max_length=255)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['-name']
        verbose_name = _('game type')
        verbose_name_plural = _('game types')


class Game(models.Model):
    name = models.CharField(_('name'), max_length=255)
    type = models.ForeignKey(
        'media.GameType',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name=_('game type'),
    )
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        verbose_name=_('owner'),
    )
    length = models.CharField(
        _('length'),
        choices=(
            ('-1h', '-1h'),
            ('1-2h', '1-2h'),
            ('2-3h', '2-3h'),
            ('3-4h', '3-4h'),
            ('4h+', '4h+'),
        ),
        max_length=255,
        blank=True,
        null=True,
    )
    min_players = models.IntegerField(
        _('minimum number of players'),
        validators=[MinValueValidator(1)],
        blank=True,
        null=True,
    )
    max_players = models.IntegerField(
        _('maximum number of players'),
        validators=[MinValueValidator(1)],
        blank=True,
        null=True,
    )
    box_length = models.FloatField(
        _('box length'),
        blank=True,
        null=True,
    )
    box_width = models.FloatField(
        _('box width'),
        blank=True,
        null=True,
    )
    box_depth = models.FloatField(
        _('box depth'),
        blank=True,
        null=True,
    )
    last_time_week_game = models.DateField(
        _('last time it was the week game'),
        blank=True,
        null=True,
    )
    comment = models.CharField(
        _('comment'),
        max_length=255,
        blank=True,
        null=True,
    )

    def __str__(self):
        return "Game {}".format(self.name)

    class Meta:
        ordering = ['-name']
        verbose_name = _('game')
        verbose_name_plural = _('games')
