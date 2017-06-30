# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-28 10:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('telephone', models.CharField(blank=True, max_length=15, null=True)),
                ('adresse', models.CharField(blank=True, max_length=255, null=True)),
                ('maxemprunt', models.IntegerField(default=5)),
                ('state', models.IntegerField(choices=[(0, 'STATE_ACTIVE'), (1, 'STATE_DISABLED'), (2, 'STATE_ARCHIVE')], default=0)),
                ('pseudo', models.CharField(help_text='Doit contenir uniquement des lettres, chiffres, ou tirets. ', max_length=32, unique=True)),
                ('comment', models.CharField(blank=True, help_text='Commentaire, promo', max_length=255)),
                ('registered', models.DateTimeField(auto_now_add=True)),
                ('right', models.IntegerField(choices=[(0, 'BASIC'), (1, 'PERM'), (2, 'BUREAU')], default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('PW', 'Mot de passe'), ('EM', 'Email')], max_length=2)),
                ('token', models.CharField(max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
