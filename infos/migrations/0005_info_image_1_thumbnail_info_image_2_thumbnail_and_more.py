# Generated by Django 4.2 on 2024-09-01 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0004_alter_info_family_2'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='image_1_thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='infos/thumbnails/'),
        ),
        migrations.AddField(
            model_name='info',
            name='image_2_thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='infos/thumbnails/'),
        ),
        migrations.AddField(
            model_name='info',
            name='image_3_thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='infos/thumbnails/'),
        ),
        migrations.AddField(
            model_name='info',
            name='image_4_thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='infos/thumbnails/'),
        ),
    ]
