# Generated by Django 4.2 on 2024-08-13 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_customuser_family'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='family',
            new_name='family_1',
        ),
    ]
