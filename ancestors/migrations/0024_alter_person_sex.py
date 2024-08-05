# Generated by Django 4.2 on 2024-08-05 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ancestors', '0023_alter_person_refn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='sex',
            field=models.CharField(blank=True, choices=[('F', 'weiblich'), ('M', 'männlich'), ('D', 'divers')], max_length=10, null=True, verbose_name='Geschlecht'),
        ),
    ]
