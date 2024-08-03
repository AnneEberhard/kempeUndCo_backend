# Generated by Django 4.2 on 2024-08-03 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ancestors', '0014_alter_person_birth_date_formatted_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FamilyTree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('kempe', 'Stammbaum Kempe'), ('huenten', 'Stammbaum Hünten')], max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='family_trees',
            field=models.ManyToManyField(blank=True, to='ancestors.familytree', verbose_name='Familienbäume'),
        ),
    ]
