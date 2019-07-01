# Generated by Django 2.1.5 on 2019-01-24 08:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    replaces = [('users', '0001_initial'),
                ('users', '0002_auto_20170629_1438'),
                ('users', '0003_auto_20170629_2156'),
                ('users', '0004_clef'),
                ('users', '0005_auto_20170703_1940'),
                ('users', '0006_clef_commentaire'),
                ('users', '0007_adhesion'),
                ('users', '0008_auto_20170705_0001'),
                ('users', '0009_auto_20171114_2303')]

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('password',
                 models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True,
                                                    verbose_name='last login')),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('email',
                 models.EmailField(blank=True, max_length=254, null=True)),
                ('telephone',
                 models.CharField(blank=True, max_length=15, null=True)),
                ('adresse',
                 models.CharField(blank=True, max_length=255, null=True)),
                ('maxemprunt', models.IntegerField(default=5)),
                ('state', models.IntegerField(
                    choices=[(0, 'STATE_ACTIVE'), (1, 'STATE_DISABLED'),
                             (2, 'STATE_ARCHIVE')], default=0)),
                ('pseudo', models.CharField(
                    help_text='Doit contenir uniquement des lettres, chiffres, ou tirets. ',
                    max_length=32, unique=True)),
                ('comment',
                 models.CharField(blank=True, help_text='Commentaire, promo',
                                  max_length=255)),
                ('registered', models.DateTimeField(auto_now_add=True)),
                ('right', models.IntegerField(
                    choices=[(0, 'BASIC'), (1, 'PERM'), (2, 'BUREAU')],
                    default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('type', models.CharField(
                    choices=[('PW', 'Mot de passe'), ('EM', 'Email')],
                    max_length=2)),
                ('token', models.CharField(max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('user',
                 models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                   to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='maxemprunt',
            field=models.IntegerField(default=5,
                                      help_text="Maximum d'emprunts autorisés"),
        ),
        migrations.RemoveField(
            model_name='user',
            name='right',
        ),
        migrations.CreateModel(
            name='ListRight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('listright', models.CharField(max_length=255, unique=True)),
                ('details',
                 models.CharField(blank=True, help_text='Description',
                                  max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Right',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('right',
                 models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                   to='users.ListRight')),
                ('user',
                 models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                   to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='right',
            unique_together={('user', 'right')},
        ),
        migrations.CreateModel(
            name='Clef',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255, unique=True)),
                ('proprio', models.ForeignKey(blank=True, null=True,
                                              on_delete=django.db.models.deletion.PROTECT,
                                              to=settings.AUTH_USER_MODEL)),
                ('commentaire',
                 models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Adhesion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('annee_debut', models.IntegerField(unique=True)),
                ('annee_fin', models.IntegerField(unique=True)),
                ('adherent', models.ManyToManyField(blank=True,
                                                    to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]