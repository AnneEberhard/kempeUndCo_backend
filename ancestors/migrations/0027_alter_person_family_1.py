# Generated by Django 4.2.15 on 2024-09-07 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ancestors', '0026_rename_family_tree_1_person_family_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='family_1',
            field=models.CharField(choices=[('kempe', 'Stammbaum Kempe'), ('huenten', 'Stammbaum Hünten')], default='kempe', max_length=100, verbose_name='Stammbaum 1'),
        ),
    ]
