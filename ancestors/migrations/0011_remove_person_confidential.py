# Generated by Django 4.2 on 2024-08-03 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ancestors', '0010_alter_person_birt_date_alter_person_deat_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='confidential',
        ),
    ]
