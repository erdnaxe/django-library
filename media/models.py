from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('name'),
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = _('author')
        verbose_name_plural = _('authors')


class Media(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name=_('title'),
    )
    side_title = models.CharField(
        max_length=31,
        verbose_name=_('side title'),
    )
    author = models.ManyToManyField(
        'Author',
        verbose_name=_('author'),
    )

    def __str__(self):
        return "Media {} de {}".format(self.title, self.author.all().first())

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
    borrowed_at = models.DateTimeField(
        help_text='%d/%m/%y %H:%M:%S',
        verbose_name=_('borrowed at'),
    )
    given_back_at = models.DateTimeField(
        help_text='%d/%m/%y %H:%M:%S',
        blank=True,
        null=True,
        verbose_name=_('given back at'),
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


class Game(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('name'),
    )
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        verbose_name=_('owner'),
    )
    length = models.CharField(
        choices=(
            ('-1h', '-1h'),
            ('1-2h', '1-2h'),
            ('2-3h', '2-3h'),
            ('3-4h', '3-4h'),
            ('4h+', '4h+'),
        ),
        max_length=255,
        verbose_name=_('length'),
    )
    min_players = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name=_('minimum number of players'),
    )
    max_players = models.IntegerField(
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
        return "Game {}".format(self.name)

    class Meta:
        ordering = ['-name']
        verbose_name = _('game')
        verbose_name_plural = _('games')
