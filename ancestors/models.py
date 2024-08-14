from django.conf import settings
from django.db import models
from datetime import datetime
from django.utils import timezone


class Person(models.Model):
    """
    A model representing a person, based on the source file from Ahnenblatt.

    Attributes that are represented in the admin panel:
    - refn (CharField): Unique reference number for the person.
    - name (CharField): Full name of the person, automatically generated and not editable.
    - uid (CharField): Unique identifier.
    - surn (CharField): Surname of the person.
    - givn (CharField): Given name of the person.
    - sex (CharField): Sex of the person, with choices of 'weiblich', 'männlich', or 'divers'.
    - occu (CharField): Occupation of the person.
    - chan_date (CharField): Date of last change.
    - chan_date_time (CharField): Date and time of last change.
    - birt_date (CharField): Birth date of the person.
    - birth_date_formatted (DateField): Automatically formatted birth date.
    - birt_plac (CharField): Birth place of the person.
    - deat_date (CharField): Death date of the person.
    - death_date_formatted (DateField): Automatically formatted death date.
    - deat_plac (CharField): Death place of the person.
    - note (TextField): Additional notes about the person.
    - chr_date (CharField): Christening date of the person.
    - chr_plac (CharField): Christening place of the person.
    - buri_date (CharField): Burial date of the person.
    - buri_plac (CharField): Burial place of the person.
    - name_rufname (CharField): Rufname (nickname or common name used).
    - name_npfx (CharField): Name prefix.
    - sour (TextField): Sources of information about the person.
    - name_nick (CharField): Nickname.
    - name_marnm (CharField): Married name.
    - chr_addr (CharField): Christening address.
    - reli (CharField): Religion.
    - 6 obje_file_X and obje_title_X fields that are for uploading up to 6 pictures

    Attributes that are still included here but are handled via the model relation 
    (s. below, created via scripts, s README for process):
    - all references to parents, children, spouses and marriages

    Attributes that were newly created via scripts only for this database:
    - family_tree_1 (CharField): The first family tree to which the person belongs, with choices from predefined options.
    - family_tree_2 (CharField): The second family tree to which the person belongs, with choices from predefined options.
    - creation_date (DateTimeField): The date and time when the person record was created.
    - last_modified_date (DateTimeField): The date and time when the person record was last modified.
    - created_by (ForeignKey): The user who created the person record.
    - last_modified_by (ForeignKey): The user who last modified the person record.
    """

    SEX_CHOICES = [
        ('F', 'weiblich'),
        ('M', 'männlich'),
        ('D', 'divers'),
    ]

    refn = models.CharField(max_length=255, unique=True, verbose_name='#REFN')
    name = models.CharField(max_length=255, verbose_name='Name', editable=False)
    fath_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Name des Vaters')
    fath_refn = models.CharField(max_length=255, null=True, blank=True, verbose_name='#REFN des Vaters')
    moth_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Name der Mutter')
    moth_refn = models.CharField(max_length=255, null=True, blank=True, verbose_name='#REFN der Mutter')
    uid = models.CharField(max_length=255, null=True, blank=True, verbose_name='UID')
    surn = models.CharField(max_length=255, null=True, blank=True, verbose_name='Nachname')
    givn = models.CharField(max_length=255, null=True, blank=True, verbose_name='Vorname')
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, null=True, blank=True, verbose_name='Geschlecht')
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

    def _generate_unique_refn(self):
        """
        Generate a unique refn value that does not conflict with existing ones.

        Iterates through existing refn values to find the maximum numerical suffix,
        increments it, and returns a new unique refn value.

        Returns:
        - string: A new unique refn value in the format '@I<new_number>@'
        """
        existing_refs = Person.objects.values_list('refn', flat=True)
        max_num = 0
        for ref in existing_refs:
            try:
                num = int(ref.strip('@I@'))
                if num > max_num:
                    max_num = num
            except ValueError:
                continue

        new_num = max_num + 1
        return f'@I{new_num}@'

    def save(self, *args, **kwargs):
        """
        Save the Person instance including metadata and automatic birth/death date generation.

        Automatically generates a unique refn for new instances, sets creation and modification dates,
        and formats the name and birth/death dates.

        Parameters:
        - user: The user who is creating or modifying the instance (optional)
        """
        user = kwargs.pop('user', None)

        if not self.pk:  # Neues Objekt
            if not self.refn:
                self.refn = self._generate_unique_refn()
            self.creation_date = timezone.now()
            if user:
                self.created_by = user
        else:  # Bestehendes Objekt
            self.last_modified_date = timezone.now()
            if user:
                self.last_modified_by = user

        # Automatisch den Name-Feld setzen
        if self.name_npfx:
            name_parts = [self.name_npfx]
        else:
            name_parts = []

        if self.givn:
            name_parts.append(self.givn)

        if self.name_nick:
            name_parts.append(f"'{self.name_nick}'")

        if self.surn:
            name_parts.append(self.surn)

        # Join the parts with a space
        self.name = " ".join(name_parts) if name_parts else "Unbekannt"

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
        """
        Return the string representation of the Person instance.

        Returns:
        - string: The name of the person
        """
        return self.name


class Relation(models.Model):
    """
    A model representing the relationships and family status of a person.

    Attributes:
    - person (ForeignKey): The person for whom the relationships are being recorded.
    - fath_refn (ForeignKey): Reference to the person's father.
    - moth_refn (ForeignKey): Reference to the person's mother.
    - marr_spou_refn_1 (ForeignKey): Reference to the person's first spouse.
    - marr_date_1 (CharField): The marriage date for the first spouse.
    - marr_plac_1 (CharField): The marriage place for the first spouse.
    - children_1 (ManyToManyField): The children from the first marriage.
    - fam_stat_1 (CharField): The family status for the first marriage.
    - marr_spou_refn_2 (ForeignKey): Reference to the person's second spouse.
    - children_2 (ManyToManyField): The children from the second marriage.
    - marr_date_2 (CharField): The marriage date for the second spouse.
    - marr_plac_2 (CharField): The marriage place for the second spouse.
    - fam_stat_2 (CharField): The family status for the second marriage.
    - marr_spou_refn_3 (ForeignKey): Reference to the person's third spouse.
    - children_3 (ManyToManyField): The children from the third marriage.
    - marr_date_3 (CharField): The marriage date for the third spouse.
    - marr_plac_3 (CharField): The marriage place for the third spouse.
    - marr_spou_refn_4 (ForeignKey): Reference to the person's fourth spouse.
    - fam_stat_3 (CharField): The family status for the third marriage.
    - children_4 (ManyToManyField): The children from the fourth marriage.
    - marr_date_4 (CharField): The marriage date for the fourth spouse.
    - marr_plac_4 (CharField): The marriage place for the fourth spouse.
    - fam_stat_4 (CharField): The family status for the fourth marriage.
    """

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
