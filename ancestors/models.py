from django.conf import settings
from django.db import models
from datetime import datetime
from django.utils import timezone

class Person(models.Model):
    refn = models.CharField(max_length=255, verbose_name='#REFN')
    name = models.CharField(max_length=255, verbose_name='Name')
    fath_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Name des Vaters')
    fath_refn = models.CharField(max_length=255, null=True, blank=True, verbose_name='#REFN des Vaters')
    moth_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Name der Mutter')
    moth_refn = models.CharField(max_length=255, null=True, blank=True, verbose_name='#REFN der Mutter')
    uid = models.CharField(max_length=255, null=True, blank=True, verbose_name='UID')
    surn = models.CharField(max_length=255, null=True, blank=True, verbose_name='Nachname')
    givn = models.CharField(max_length=255, null=True, blank=True, verbose_name='Vorname')
    sex = models.CharField(max_length=10, null=True, blank=True, verbose_name='Geschlecht')
    occu = models.CharField(max_length=255, null=True, blank=True, verbose_name='Beruf')
    chan_date = models.CharField(max_length=255, null=True, blank=True, verbose_name='Änderungsdatum')
    chan_date_time = models.CharField(max_length=255, null=True, blank=True, verbose_name='Änderungsdatum und -uhrzeit')
    birt_date = models.CharField(max_length=255, null=True, blank=True, verbose_name='Geburtsdatum')
    birth_date_formatted = models.DateField(null=True, blank=True, verbose_name='Automatisch formatiertes Geburtsdatum')
    birt_plac = models.CharField(max_length=255, null=True, blank=True, verbose_name='Geburtsort')
    deat_date = models.CharField(max_length=255, null=True, blank=True, verbose_name='Sterbedatum')
    death_date_formatted = models.DateField(null=True, blank=True, verbose_name='Automatisch formatiertes Sterbedatum')
    deat_plac = models.CharField(max_length=255, null=True, blank=True, verbose_name='Sterbeort')
    note = models.TextField(null=True, blank=True, verbose_name='Notizen')
    chr_date = models.CharField(max_length=255, null=True, blank=True, verbose_name='Taufe Datum')
    chr_plac = models.CharField(max_length=255, null=True, blank=True, verbose_name='Taufe Ort')
    buri_date = models.CharField(max_length=255, null=True, blank=True, verbose_name='Beerdigungsdatum')
    buri_plac = models.CharField(max_length=255, null=True, blank=True, verbose_name='Beerdigungsort')
    name_rufname = models.CharField(max_length=255, null=True, blank=True, verbose_name='Rufname')
    name_npfx = models.CharField(max_length=255, null=True, blank=True, verbose_name='Namenspräfix')
    sour = models.TextField(null=True, blank=True, verbose_name='Quellen')
    name_nick = models.CharField(max_length=255, null=True, blank=True, verbose_name='Spitzname')
    name_marnm = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ehename')
    chr_addr = models.CharField(max_length=255, null=True, blank=True, verbose_name='Taufe Adresse')
    reli = models.CharField(max_length=255, null=True, blank=True, verbose_name='Religion')

    # Marriage and family information (repeated fields for each spouse and family)
    marr_spou_name_1 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Name des Ehepartners 1')
    marr_spou_refn_1 = models.CharField(max_length=255, null=True, blank=True, verbose_name='#REFN des Ehepartners 1')
    fam_husb_1 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ehemann der Familie 1')
    fam_wife_1 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ehefrau der Familie 1')
    marr_date_1 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Heiratsdatum 1')
    marr_plac_1 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Heiratsort 1')
    fam_chil_1 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Kinder der Familie 1')
    fam_marr_1 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ehe der Familie 1')
    fam_stat_1 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Familienstand 1')

    marr_spou_name_2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Name des Ehepartners 2')
    marr_spou_refn_2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='#REFN des Ehepartners 2')
    fam_husb_2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ehemann der Familie 2')
    fam_wife_2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ehefrau der Familie 2')
    marr_date_2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Heiratsdatum 2')
    marr_plac_2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Heiratsort 2')
    fam_chil_2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Kinder der Familie 2')
    fam_marr_2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ehe der Familie 2')
    fam_stat_2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Familienstand 2')

    marr_spou_name_3 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Name des Ehepartners 3')
    marr_spou_refn_3 = models.CharField(max_length=255, null=True, blank=True, verbose_name='#REFN des Ehepartners 3')
    fam_husb_3 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ehemann der Familie 3')
    fam_wife_3 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ehefrau der Familie 3')
    marr_date_3 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Heiratsdatum 3')
    marr_plac_3 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Heiratsort 3')
    fam_chil_3 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Kinder der Familie 3')
    fam_marr_3 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ehe der Familie 3')
    fam_stat_3 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Familienstand 3')

    marr_spou_name_4 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Name des Ehepartners 4')
    marr_spou_refn_4 = models.CharField(max_length=255, null=True, blank=True, verbose_name='#REFN des Ehepartners 4')
    fam_husb_4 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ehemann der Familie 4')
    fam_wife_4 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ehefrau der Familie 4')
    marr_date_4 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Heiratsdatum 4')
    marr_plac_4 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Heiratsort 4')
    fam_chil_4 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Kinder der Familie 4')
    fam_marr_4 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ehe der Familie 4')
    fam_stat_4 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Familienstand 4')

    # Object files and titles
    obje_file_1 = models.FileField(upload_to='images/', null=True, blank=True, verbose_name='Bilddatei 1')
    obje_titl_1 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Bildtitel 1')
    obje_file_2 = models.FileField(upload_to='images/', null=True, blank=True, verbose_name='Bilddatei 2')
    obje_titl_2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Bildtitel 2')
    obje_file_3 = models.FileField(upload_to='images/', null=True, blank=True, verbose_name='Bilddatei 3')
    obje_titl_3 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Bildtitel 3')
    obje_file_4 = models.FileField(upload_to='images/', null=True, blank=True, verbose_name='Bilddatei 4')
    obje_titl_4 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Bildtitel 4')
    obje_file_5 = models.FileField(upload_to='images/', null=True, blank=True, verbose_name='Bilddatei 5')
    obje_titl_5 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Bildtitel 5')
    obje_file_6 = models.FileField(upload_to='images/', null=True, blank=True, verbose_name='Bilddatei 6')
    obje_titl_6 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Bildtitel 6')

    CONFIDENTIALITY_CHOICES = [
        ('no', 'Nein'),
        ('restricted', 'Eingeschränkt'),
        ('yes', 'Ja'),
    ]

    confidential = models.CharField(
        max_length=10,
        choices=CONFIDENTIALITY_CHOICES,
        default='no',
        verbose_name='Vertraulichkeit'
    )

    FAMILY_TREE_CHOICES = [
        ('kempe', 'Stammbaum Kempe'),
        ('huenten', 'Stammbaum Hünten'),
        # Weitere Familienbäume hinzufügen, wenn nötig
    ]

    family_tree_1 = models.CharField(max_length=255, choices=FAMILY_TREE_CHOICES, blank=True, null=True, verbose_name='Stammbaum 1')
    family_tree_2 = models.CharField(max_length=255, choices=FAMILY_TREE_CHOICES, blank=True, null=True, verbose_name='Stammbaum 2')

    creation_date = models.DateTimeField(default=timezone.now, verbose_name='Erstellungsdatum')
    last_modified_date = models.DateTimeField(default=timezone.now, verbose_name='Letzte Änderung')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_persons', verbose_name='Ersteller')
    last_modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_persons', verbose_name='Letzte Änderung durch')

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        if not self.pk:  # Neues Objekt
            self.creation_date = timezone.now()
            if user:
                self.created_by = user
        else:  # Bestehendes Objekt
            self.last_modified_date = timezone.now()
            if user:
                self.last_modified_by = user

        # Geburts- und Todesdaten formatieren
        if self.birt_date:
            try:
                birth_date = datetime.strptime(self.birt_date, '%d.%m.%Y').date()
                self.birth_date_formatted = birth_date
            except ValueError:
                self.birth_date_formatted = None
        if self.deat_date:
            try:
                death_date = datetime.strptime(self.deat_date, '%d.%m.%Y').date()
                self.death_date_formatted = death_date
            except ValueError:
                self.death_date_formatted = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Relation(models.Model):

    FAMILY_STATUS_CHOICES = [
        ('married', 'verheiratet'),
        ('not_married', 'nicht verheiratet'),
        ('widowed', 'verwitwet'),
        ('divorced', 'geschieden'),
    ]

    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='related_data')
    fath_refn = models.ForeignKey(Person, on_delete=models.SET_NULL, related_name='father_of', null=True, blank=True, verbose_name='Vater')
    moth_refn = models.ForeignKey(Person, on_delete=models.SET_NULL, related_name='mother_of', null=True, blank=True, verbose_name='Mutter')
    marr_spou_refn_1 = models.ForeignKey(Person, on_delete=models.SET_NULL, related_name='spouse1_of', null=True, blank=True, verbose_name='Ehepartner 1')
    marr_date_1 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Heiratsdatum 1')
    marr_plac_1 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Heiratsort 1')
    children_1 = models.ManyToManyField(Person, related_name='children_of_spouse1', blank=True, verbose_name='Kinder aus Ehe 1')
    fam_stat_1 = models.CharField(max_length=255, choices=FAMILY_STATUS_CHOICES, null=True, blank=True, verbose_name='Familienstand 1')
    marr_spou_refn_2 = models.ForeignKey(Person, on_delete=models.SET_NULL, related_name='spouse2_of', null=True, blank=True, verbose_name='Ehepartner 2')
    children_2 = models.ManyToManyField(Person, related_name='children_of_spouse2', blank=True, verbose_name='Kinder aus Ehe 2')
    marr_date_2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Heiratsdatum 2')
    marr_plac_2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Heiratsort 2')
    fam_stat_2 = models.CharField(max_length=255, choices=FAMILY_STATUS_CHOICES, null=True, blank=True, verbose_name='Familienstand 2')
    marr_spou_refn_3 = models.ForeignKey(Person, on_delete=models.SET_NULL, related_name='spouse3_of', null=True, blank=True, verbose_name='Ehepartner 3')
    children_3 = models.ManyToManyField(Person, related_name='children_of_spouse3', blank=True, verbose_name='Kinder aus Ehe 3')
    marr_date_3 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Heiratsdatum 3')
    marr_plac_3 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Heiratsort 3')
    marr_spou_refn_4 = models.ForeignKey(Person, on_delete=models.SET_NULL, related_name='spouse4_of', null=True, blank=True, verbose_name='Ehepartner 4')
    fam_stat_3 = models.CharField(max_length=255, choices=FAMILY_STATUS_CHOICES, null=True, blank=True, verbose_name='Familienstand 3')
    children_4 = models.ManyToManyField(Person, related_name='children_of_spouse4', blank=True, verbose_name='Kinder aus Ehe 4')
    marr_date_4 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Heiratsdatum 4')
    marr_plac_4 = models.CharField(max_length=255, null=True, blank=True, verbose_name='Heiratsort 4')
    fam_stat_4 = models.CharField(max_length=255, choices=FAMILY_STATUS_CHOICES, null=True, blank=True, verbose_name='Familienstand 4')
