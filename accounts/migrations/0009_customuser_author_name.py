# Generated by Django 4.2.15 on 2024-09-24 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_customuser_family_2'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='author_name',
            field=models.CharField(blank=True, default='username', max_length=255, null=True),
        ),
    ]
