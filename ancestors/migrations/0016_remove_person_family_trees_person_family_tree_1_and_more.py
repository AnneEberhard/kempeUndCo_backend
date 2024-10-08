# Generated by Django 4.2 on 2024-08-03 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ancestors', '0015_familytree_person_family_trees'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='family_trees',
        ),
        migrations.AddField(
            model_name='person',
            name='family_tree_1',
            field=models.CharField(blank=True, choices=[('kempe', 'Stammbaum Kempe'), ('huenten', 'Stammbaum Hünten')], max_length=255, null=True, verbose_name='Stammbaum 1'),
        ),
        migrations.AddField(
            model_name='person',
            name='family_tree_2',
            field=models.CharField(blank=True, choices=[('kempe', 'Stammbaum Kempe'), ('huenten', 'Stammbaum Hünten')], max_length=255, null=True, verbose_name='Stammbaum 2'),
        ),
        migrations.DeleteModel(
            name='FamilyTree',
        ),
    ]
