from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    name = models.CharField(_('name'), max_length=255, unique=True)

    def __str__(self):
        return "Author {}".format(self.name)

    class Meta:
        ordering = ['-name']
        verbose_name = _('author')
        verbose_name_plural = _('authors')


class Media(models.Model):
    title = models.CharField(_('title'), max_length=255)
    side_title = models.CharField(_('side title'), max_length=31)
    author = models.ManyToManyField('Author', verbose_name=_('author'))

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


class Game(models.Model):
    name = models.CharField(_('name'), max_length=255)
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
    )
    min_players = models.IntegerField(
        _('minimum number of players'),
        validators=[MinValueValidator(1)],
    )
    max_players = models.IntegerField(
        _('maximum number of players'),
        validators=[MinValueValidator(1)],
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
