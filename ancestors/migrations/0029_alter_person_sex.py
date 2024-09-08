# Generated by Django 4.2.15 on 2024-09-08 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ancestors', '0028_alter_person_family_1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='sex',
            field=models.CharField(choices=[('F', 'weiblich'), ('M', 'männlich'), ('D', 'divers')], default='D', max_length=10, verbose_name='Geschlecht'),
        ),
    ]
