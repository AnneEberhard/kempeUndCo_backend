# Generated by Django 4.2 on 2024-08-11 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='GUARANTOR',
        ),
        migrations.AddField(
            model_name='customuser',
            name='guarantor',
            field=models.BooleanField(default=False),
        ),
    ]
