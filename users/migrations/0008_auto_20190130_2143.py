# Generated by Django 2.1.5 on 2019-01-30 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_translate_membership_key'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='key',
            options={'ordering': ['name'], 'verbose_name': 'key', 'verbose_name_plural': 'keys'},
        ),
        migrations.AlterModelOptions(
            name='membership',
            options={'ordering': ['-start_at'], 'verbose_name': 'membership', 'verbose_name_plural': 'memberships'},
        ),
    ]
