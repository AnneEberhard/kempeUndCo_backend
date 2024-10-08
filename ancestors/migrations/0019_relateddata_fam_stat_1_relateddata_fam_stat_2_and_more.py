# Generated by Django 4.2 on 2024-08-04 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ancestors', '0018_relateddata_children_1_relateddata_children_2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='relateddata',
            name='fam_stat_1',
            field=models.CharField(blank=True, choices=[('married', 'verheiratet'), ('not_married', 'nicht verheiratet'), ('widowed', 'verwitwet'), ('divorced', 'geschieden')], max_length=255, null=True, verbose_name='Familienstand 1'),
        ),
        migrations.AddField(
            model_name='relateddata',
            name='fam_stat_2',
            field=models.CharField(blank=True, choices=[('married', 'verheiratet'), ('not_married', 'nicht verheiratet'), ('widowed', 'verwitwet'), ('divorced', 'geschieden')], max_length=255, null=True, verbose_name='Familienstand 2'),
        ),
        migrations.AddField(
            model_name='relateddata',
            name='fam_stat_3',
            field=models.CharField(blank=True, choices=[('married', 'verheiratet'), ('not_married', 'nicht verheiratet'), ('widowed', 'verwitwet'), ('divorced', 'geschieden')], max_length=255, null=True, verbose_name='Familienstand 3'),
        ),
        migrations.AddField(
            model_name='relateddata',
            name='fam_stat_4',
            field=models.CharField(blank=True, choices=[('married', 'verheiratet'), ('not_married', 'nicht verheiratet'), ('widowed', 'verwitwet'), ('divorced', 'geschieden')], max_length=255, null=True, verbose_name='Familienstand 4'),
        ),
        migrations.AddField(
            model_name='relateddata',
            name='marr_date_1',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Heiratsdatum 1'),
        ),
        migrations.AddField(
            model_name='relateddata',
            name='marr_date_2',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Heiratsdatum 2'),
        ),
        migrations.AddField(
            model_name='relateddata',
            name='marr_date_3',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Heiratsdatum 3'),
        ),
        migrations.AddField(
            model_name='relateddata',
            name='marr_date_4',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Heiratsdatum 4'),
        ),
        migrations.AddField(
            model_name='relateddata',
            name='marr_plac_1',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Heiratsort 1'),
        ),
        migrations.AddField(
            model_name='relateddata',
            name='marr_plac_2',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Heiratsort 2'),
        ),
        migrations.AddField(
            model_name='relateddata',
            name='marr_plac_3',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Heiratsort 3'),
        ),
        migrations.AddField(
            model_name='relateddata',
            name='marr_plac_4',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Heiratsort 4'),
        ),
    ]
