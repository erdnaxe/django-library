# Generated by Django 2.1.5 on 2019-01-27 18:21

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('media', '0004_translate'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Emprunt',
            new_name='BorrowedMedia',
        ),
    ]
