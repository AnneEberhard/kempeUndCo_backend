# Generated by Django 4.2 on 2024-08-23 16:29

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('infos', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Entry',
            new_name='Info',
        ),
    ]
