# Generated by Django 2.1.5 on 2019-01-27 16:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_user_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adhesion',
            old_name='member',
            new_name='members',
        ),
        migrations.AlterField(
            model_name='adhesion',
            name='members',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='members'),
        ),
    ]
