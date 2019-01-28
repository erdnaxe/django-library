# Generated by Django 2.1.5 on 2019-01-28 19:14

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('media', '0003_auto_20190127_1624'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Auteur',
            new_name='Author',
        ),
        migrations.RenameModel(
            old_name='Jeu',
            new_name='Game',
        ),
        migrations.RenameModel(
            old_name='Emprunt',
            new_name='BorrowedMedia',
        ),
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['-name'], 'verbose_name': 'author', 'verbose_name_plural': 'authors'},
        ),
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ['-name'], 'verbose_name': 'game', 'verbose_name_plural': 'games'},
        ),
        migrations.AlterModelOptions(
            name='media',
            options={'ordering': ['-title'], 'verbose_name': 'media', 'verbose_name_plural': 'media'},
        ),
        migrations.RenameField(
            model_name='author',
            old_name='nom',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='nom',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='media',
            old_name='titre',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='media',
            old_name='auteur',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='media',
            old_name='cote',
            new_name='side_title',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='proprietaire',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='duree',
            new_name='length',
        ),
        migrations.AlterModelOptions(
            name='borrowedmedia',
            options={'ordering': ['-borrowed_at'], 'permissions': (('my_view', 'Can view his borrowed media'),), 'verbose_name': 'borrowed media', 'verbose_name_plural': 'borrowed medias'},
        ),
        migrations.RenameField(
            model_name='borrowedmedia',
            old_name='date_emprunt',
            new_name='borrowed_at',
        ),
        migrations.RenameField(
            model_name='borrowedmedia',
            old_name='date_rendu',
            new_name='given_back_at',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='nombre_joueurs_min',
            new_name='min_players',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='nombre_joueurs_max',
            new_name='max_players',
        ),
        migrations.RenameField(
            model_name='borrowedmedia',
            old_name='permanencier_emprunt',
            new_name='borrowed_with_permanent',
        ),
        migrations.RenameField(
            model_name='borrowedmedia',
            old_name='permanencier_rendu',
            new_name='given_back_with_permanent',
        ),
    ]
