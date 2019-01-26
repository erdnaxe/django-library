# Generated by Django 2.1.5 on 2019-01-26 10:44

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0001_initial_squashed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='auteur',
            options={'ordering': ['-nom'], 'permissions': (('add', 'Can add an author'), ('change', 'Can edit an author'), ('delete', 'Can delete an author'), ('view', 'Can view an author')), 'verbose_name': 'media', 'verbose_name_plural': 'media'},
        ),
        migrations.AlterModelOptions(
            name='emprunt',
            options={'ordering': ['-date_emprunt'], 'permissions': (('add', 'Can add a borrowed media'), ('change', 'Can edit a borrowed media'), ('delete', 'Can delete a borrowed media'), ('view', 'Can view a borrowed media')), 'verbose_name': 'borrowed media', 'verbose_name_plural': 'borrowed media'},
        ),
        migrations.AlterModelOptions(
            name='jeu',
            options={'ordering': ['-nom'], 'permissions': (('add', 'Can add a game'), ('change', 'Can edit a game'), ('delete', 'Can delete a game'), ('view', 'Can view a game')), 'verbose_name': 'game', 'verbose_name_plural': 'games'},
        ),
        migrations.AlterModelOptions(
            name='media',
            options={'ordering': ['-titre'], 'permissions': (('add', 'Can add a media'), ('change', 'Can edit a media'), ('delete', 'Can delete a media'), ('view', 'Can view a media')), 'verbose_name': 'media', 'verbose_name_plural': 'media'},
        ),
        migrations.AlterField(
            model_name='auteur',
            name='nom',
            field=models.CharField(max_length=255, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='emprunt',
            name='date_emprunt',
            field=models.DateTimeField(help_text='%d/%m/%y %H:%M:%S', verbose_name='borrowed at'),
        ),
        migrations.AlterField(
            model_name='emprunt',
            name='date_rendu',
            field=models.DateTimeField(blank=True, help_text='%d/%m/%y %H:%M:%S', null=True, verbose_name='given back at'),
        ),
        migrations.AlterField(
            model_name='emprunt',
            name='media',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='media.Media', verbose_name='media'),
        ),
        migrations.AlterField(
            model_name='emprunt',
            name='permanencier_emprunt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_permanencier_emprunt', to=settings.AUTH_USER_MODEL, verbose_name='borrowed with permanent'),
        ),
        migrations.AlterField(
            model_name='emprunt',
            name='permanencier_rendu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_permanencier_rendu', to=settings.AUTH_USER_MODEL, verbose_name='given back with permanent'),
        ),
        migrations.AlterField(
            model_name='emprunt',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='borrower'),
        ),
        migrations.AlterField(
            model_name='jeu',
            name='comment',
            field=models.CharField(blank=True, help_text='Commentaire', max_length=255, null=True, verbose_name='comment'),
        ),
        migrations.AlterField(
            model_name='jeu',
            name='duree',
            field=models.CharField(choices=[('-1h', '-1h'), ('1-2h', '1-2h'), ('2-3h', '2-3h'), ('3-4h', '3-4h'), ('4h+', '4h+')], max_length=255, verbose_name='length'),
        ),
        migrations.AlterField(
            model_name='jeu',
            name='nom',
            field=models.CharField(max_length=255, verbose_name='nom'),
        ),
        migrations.AlterField(
            model_name='jeu',
            name='nombre_joueurs_max',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='maximum number of players'),
        ),
        migrations.AlterField(
            model_name='jeu',
            name='nombre_joueurs_min',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='minimum number of players'),
        ),
        migrations.AlterField(
            model_name='jeu',
            name='proprietaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
        migrations.AlterField(
            model_name='media',
            name='auteur',
            field=models.ManyToManyField(to='media.Auteur', verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='media',
            name='cote',
            field=models.CharField(max_length=31, verbose_name='side title'),
        ),
        migrations.AlterField(
            model_name='media',
            name='titre',
            field=models.CharField(max_length=255, verbose_name='title'),
        ),
        migrations.AlterModelOptions(
            name='auteur',
            options={'ordering': ['-nom'], 'permissions': (('add', 'Can add an author'), ('change', 'Can edit an author'), ('delete', 'Can delete an author'), ('view', 'Can view an author')), 'verbose_name': 'author', 'verbose_name_plural': 'authors'},
        ),
        migrations.AlterField(
            model_name='jeu',
            name='comment',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='comment'),
        ),
        migrations.AlterField(
            model_name='jeu',
            name='nom',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
    ]