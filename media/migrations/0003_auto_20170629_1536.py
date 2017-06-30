# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 13:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0002_media_auteur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emprunt',
            name='date_rendu',
            field=models.DateTimeField(blank=True, help_text='%d/%m/%y %H:%M:%S'),
        ),
        migrations.AlterField(
            model_name='emprunt',
            name='permanencier_rendu',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_permanencier_rendu', to=settings.AUTH_USER_MODEL),
        ),
    ]
