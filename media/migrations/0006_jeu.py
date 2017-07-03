# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-03 14:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('media', '0005_auto_20170630_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jeu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('duree', models.CharField(choices=[('LONG', 'LONG'), ('MOYEN', 'MOYEN'), ('COURT', 'COURT')], max_length=255)),
                ('nombre_joueurs_min', models.IntegerField()),
                ('nombre_joueurs_max', models.IntegerField()),
                ('comment', models.CharField(blank=True, help_text='Commentaire', max_length=255, null=True)),
                ('proprietaire', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
