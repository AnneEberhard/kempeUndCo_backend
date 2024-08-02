# Generated by Django 4.2 on 2024-08-02 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ancestors', '0005_alter_person_obje_file_2_alter_person_obje_file_3_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='obje_file_1',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Bilddatei 1'),
        ),
        migrations.AlterField(
            model_name='person',
            name='obje_file_2',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Bilddatei 2'),
        ),
        migrations.AlterField(
            model_name='person',
            name='obje_file_3',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Bilddatei 3'),
        ),
        migrations.AlterField(
            model_name='person',
            name='obje_file_4',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Bilddatei 4'),
        ),
        migrations.AlterField(
            model_name='person',
            name='obje_file_5',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Bilddatei 5'),
        ),
        migrations.AlterField(
            model_name='person',
            name='obje_file_6',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Bilddatei 6'),
        ),
    ]
