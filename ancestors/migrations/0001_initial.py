# Generated by Django 4.2 on 2024-08-02 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refn', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('fath_name', models.CharField(blank=True, max_length=255, null=True)),
                ('fath_refn', models.CharField(blank=True, max_length=255, null=True)),
                ('moth_name', models.CharField(blank=True, max_length=255, null=True)),
                ('moth_refn', models.CharField(blank=True, max_length=255, null=True)),
                ('uid', models.CharField(blank=True, max_length=255, null=True)),
                ('surn', models.CharField(blank=True, max_length=255, null=True)),
                ('givn', models.CharField(blank=True, max_length=255, null=True)),
                ('sex', models.CharField(blank=True, max_length=10, null=True)),
                ('occu', models.CharField(blank=True, max_length=255, null=True)),
                ('chan_date', models.DateField(blank=True, null=True)),
                ('chan_date_time', models.CharField(blank=True, max_length=255, null=True)),
                ('birt_date', models.DateField(blank=True, null=True)),
                ('birt_plac', models.CharField(blank=True, max_length=255, null=True)),
                ('deat_date', models.DateField(blank=True, null=True)),
                ('deat_plac', models.CharField(blank=True, max_length=255, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('chr_date', models.DateField(blank=True, null=True)),
                ('chr_plac', models.CharField(blank=True, max_length=255, null=True)),
                ('buri_date', models.DateField(blank=True, null=True)),
                ('buri_plac', models.CharField(blank=True, max_length=255, null=True)),
                ('name_rufname', models.CharField(blank=True, max_length=255, null=True)),
                ('name_npfx', models.CharField(blank=True, max_length=255, null=True)),
                ('sour', models.TextField(blank=True, null=True)),
                ('name_nick', models.CharField(blank=True, max_length=255, null=True)),
                ('name_marnm', models.CharField(blank=True, max_length=255, null=True)),
                ('chr_addr', models.CharField(blank=True, max_length=255, null=True)),
                ('reli', models.CharField(blank=True, max_length=255, null=True)),
                ('marr_spou_name_1', models.CharField(blank=True, max_length=255, null=True)),
                ('marr_spou_refn_1', models.CharField(blank=True, max_length=255, null=True)),
                ('fam_husb_1', models.CharField(blank=True, max_length=255, null=True)),
                ('fam_wife_1', models.CharField(blank=True, max_length=255, null=True)),
                ('marr_date_1', models.DateField(blank=True, null=True)),
                ('marr_plac_1', models.CharField(blank=True, max_length=255, null=True)),
                ('fam_chil_1', models.CharField(blank=True, max_length=255, null=True)),
                ('fam_stat_1', models.CharField(blank=True, max_length=255, null=True)),
                ('fam_marr_1', models.CharField(blank=True, max_length=255, null=True)),
                ('marr_spou_name_2', models.CharField(blank=True, max_length=255, null=True)),
                ('marr_spou_refn_2', models.CharField(blank=True, max_length=255, null=True)),
                ('fam_husb_2', models.CharField(blank=True, max_length=255, null=True)),
                ('fam_wife_2', models.CharField(blank=True, max_length=255, null=True)),
                ('marr_date_2', models.DateField(blank=True, null=True)),
                ('marr_plac_2', models.CharField(blank=True, max_length=255, null=True)),
                ('fam_chil_2', models.CharField(blank=True, max_length=255, null=True)),
                ('fam_stat_2', models.CharField(blank=True, max_length=255, null=True)),
                ('fam_marr_2', models.CharField(blank=True, max_length=255, null=True)),
                ('marr_spou_name_3', models.CharField(blank=True, max_length=255, null=True)),
                ('marr_spou_refn_3', models.CharField(blank=True, max_length=255, null=True)),
                ('fam_husb_3', models.CharField(blank=True, max_length=255, null=True)),
                ('fam_wife_3', models.CharField(blank=True, max_length=255, null=True)),
                ('marr_date_3', models.DateField(blank=True, null=True)),
                ('marr_plac_3', models.CharField(blank=True, max_length=255, null=True)),
                ('fam_chil_3', models.CharField(blank=True, max_length=255, null=True)),
                ('fam_stat_3', models.CharField(blank=True, max_length=255, null=True)),
                ('fam_marr_3', models.CharField(blank=True, max_length=255, null=True)),
                ('marr_spou_name_4', models.CharField(blank=True, max_length=255, null=True)),
                ('marr_spou_refn_4', models.CharField(blank=True, max_length=255, null=True)),
                ('fam_husb_4', models.CharField(blank=True, max_length=255, null=True)),
                ('fam_wife_4', models.CharField(blank=True, max_length=255, null=True)),
                ('marr_date_4', models.DateField(blank=True, null=True)),
                ('marr_plac_4', models.CharField(blank=True, max_length=255, null=True)),
                ('fam_chil_4', models.CharField(blank=True, max_length=255, null=True)),
                ('fam_stat_4', models.CharField(blank=True, max_length=255, null=True)),
                ('fam_marr_4', models.CharField(blank=True, max_length=255, null=True)),
                ('obje_file_1', models.CharField(blank=True, max_length=255, null=True)),
                ('obje_titl_1', models.CharField(blank=True, max_length=255, null=True)),
                ('obje_file_2', models.CharField(blank=True, max_length=255, null=True)),
                ('obje_titl_2', models.CharField(blank=True, max_length=255, null=True)),
                ('obje_file_3', models.CharField(blank=True, max_length=255, null=True)),
                ('obje_titl_3', models.CharField(blank=True, max_length=255, null=True)),
                ('obje_file_4', models.CharField(blank=True, max_length=255, null=True)),
                ('obje_titl_4', models.CharField(blank=True, max_length=255, null=True)),
                ('obje_file_5', models.CharField(blank=True, max_length=255, null=True)),
                ('obje_titl_5', models.CharField(blank=True, max_length=255, null=True)),
                ('obje_file_6', models.CharField(blank=True, max_length=255, null=True)),
                ('obje_titl_6', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
