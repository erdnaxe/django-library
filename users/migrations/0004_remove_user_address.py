# Generated by Django 2.1.5 on 2019-01-27 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_translate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
    ]