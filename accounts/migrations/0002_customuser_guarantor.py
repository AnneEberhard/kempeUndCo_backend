# Generated by Django 4.2 on 2024-07-30 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='GUARANTOR',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
