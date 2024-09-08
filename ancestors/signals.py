import os
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save, m2m_changed

from .tasks import rename_image
from .models import Person, Relation


@receiver(post_save, sender=Person)
def rename_files_on_save(sender, instance, created, **kwargs):
    """
    After saving a Person instance, this function renames associated file fields.

    This function checks if any file fields (obje_file_1 to obje_file_6) are present on the instance.
    If files are found, their names are altered based on the instance's attributes. The old file paths
    are then renamed to the new paths within the MEDIA_ROOT directory. The database fields are updated
    with the new file names. To avoid recursive calls to this post-save signal, a flag
    (_performing_post_save) is used.

    Parameters:
    - sender: The model class (Person) that sent the signal.
    - instance: The instance of the Person being saved.
    - created: A boolean indicating if the instance was created (True) or updated (False).
    - kwargs: Additional keyword arguments.
    """
    if not hasattr(instance, '_performing_post_save'):
        instance._performing_post_save = False

    if not instance._performing_post_save:
        instance._performing_post_save = True

        for i in range(1, 7):
            field_name = f'obje_file_{i}'
            file_field = getattr(instance, field_name)

            if file_field and file_field.name:
                # Old file path
                old_path = file_field.path
                # New file path
                new_path = rename_image(instance, file_field.name, i)
                # Full path within MEDIA_ROOT
                new_full_path = os.path.join(settings.MEDIA_ROOT, new_path)

                # Rename the file
                if os.path.exists(old_path) and old_path != new_full_path:
                    os.rename(old_path, new_full_path)

                    # Update the path in the database field
                    file_field.name = new_path

        instance.save(update_fields=[f'obje_file_{i}' for i in range(1, 7)])
        instance._performing_post_save = False


@receiver(pre_save, sender=Person)
def delete_old_files_on_update(sender, instance, **kwargs):
    """
    Before saving an updated Person instance, this function deletes old files.

    This function checks if the Person instance already exists in the database (by checking the primary key).
    If the instance exists and the file fields (obje_file_1 to obje_file_6) are being updated, the old files
    associated with these fields are deleted from the file system.

    Parameters:
    - sender: The model class (Person) that sent the signal.
    - instance: The instance of the Person being updated.
    - kwargs: Additional keyword arguments.
    """
    if not instance.pk:
        return False  # No action needed for new instances

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return False  # Old instance does not exist, no action needed

    for i in range(1, 7):
        field_name = f'obje_file_{i}'
        old_file = getattr(old_instance, field_name)
        new_file = getattr(instance, field_name)

        if old_file and old_file != new_file:
            if os.path.exists(old_file.path):
                os.remove(old_file.path)


@receiver(post_delete, sender=Person)
def delete_files_on_delete(sender, instance, **kwargs):
    """
    After a Person instance is deleted, this function removes associated files from the file system.

    This function iterates over the file fields (obje_file_1 to obje_file_6) and deletes the files from
    the file system if they exist.

    Parameters:
    - sender: The model class (Person) that sent the signal.
    - instance: The instance of the Person being deleted.
    - kwargs: Additional keyword arguments.
    """
    for i in range(1, 7):
        field_name = f'obje_file_{i}'
        file_field = getattr(instance, field_name)
        if file_field and file_field.name:
            file_path = file_field.path
            if os.path.exists(file_path):
                os.remove(file_path)


@receiver(post_save, sender=Relation)
def update_own_person_fields(sender, instance, **kwargs):
    if instance.fath_refn:
        print(instance.fath_refn.refn)
        instance.person.fath_refn = instance.fath_refn.refn
    if instance.moth_refn:
        instance.person.moth_refn = instance.moth_refn.refn
    if instance.marr_spou_refn_1:
        instance.person.marr_spou_refn_1 = instance.marr_spou_refn_1.refn
        instance.person.marr_date_1 = instance.marr_date_1
        instance.person.marr_plac_1 = instance.marr_plac_1
    if instance.marr_spou_refn_2:
        instance.person.marr_spou_refn_2 = instance.marr_spou_refn_2.refn
        instance.person.marr_date_2 = instance.marr_date_2
        instance.person.marr_plac_2 = instance.marr_plac_2
    if instance.marr_spou_refn_3:
        instance.person.marr_spou_refn_3 = instance.marr_spou_refn_3.refn
        instance.person.marr_date_3 = instance.marr_date_3
        instance.person.marr_plac_3 = instance.marr_plac_3
    if instance.marr_spou_refn_4:
        instance.person.marr_spou_refn_4 = instance.marr_spou_refn_4.refn
        instance.person.marr_date_4 = instance.marr_date_4
        instance.person.marr_plac_4 = instance.marr_plac_4
    if instance.children_1.exists():
        instance.person.fam_chil_1 = ','.join(child.refn for child in instance.children_1.all())
    if instance.children_2.exists():
        instance.person.fam_chil_2 = ','.join(child.refn for child in instance.children_1.all())
    if instance.children_3.exists():
        instance.person.fam_chil_3 = ','.join(child.refn for child in instance.children_1.all())
    if instance.children_4.exists():
        instance.person.fam_chil_4 = ','.join(child.refn for child in instance.children_1.all())

    instance.person.save()


@receiver(post_save, sender=Relation)
def update_child_person_fields(sender, instance, **kwargs):
    for child in instance.children_1.all():
        if instance.person.sex == 'F':
            child.moth_refn = instance.person.refn
            if instance.marr_spou_refn_1:
                child.fath_refn = instance.marr_spou_refn_1.refn
        else:
            child.fath_refn = instance.person.refn
            if instance.marr_spou_refn_1:
                child.moth_refn = instance.marr_spou_refn_1.refn
        child.save()
    for child in instance.children_2.all():
        if instance.person.sex == 'F':
            child.moth_refn = instance.person.refn
            if instance.marr_spou_refn_2:
                child.fath_refn = instance.marr_spou_refn_2.refn
        else:
            child.fath_refn = instance.person.refn
            if instance.marr_spou_refn_2:
                child.moth_refn = instance.marr_spou_refn_2.refn
        child.save()
    for child in instance.children_3.all():
        if instance.person.sex == 'F':
            child.moth_refn = instance.person.refn
            if instance.marr_spou_refn_3:
                child.fath_refn = instance.marr_spou_refn_3.refn
        else:
            child.fath_refn = instance.person.refn
            if instance.marr_spou_refn_3:
                child.moth_refn = instance.marr_spou_refn_3.refn
        child.save()
    for child in instance.children_4.all():
        if instance.person.sex == 'F':
            child.moth_refn = instance.person.refn
            if instance.marr_spou_refn_4:
                child.fath_refn = instance.marr_spou_refn_4.refn
        else:
            child.fath_refn = instance.person.refn
            if instance.marr_spou_refn_4:
                child.moth_refn = instance.marr_spou_refn_4.refn
        child.save()


@receiver(post_save, sender=Relation)
def update_spouse_person_fields(sender, instance, **kwargs):

    def update_spouse(spouse_field, spouse_date, spouse_place, children_field, next_spouse_field):
        spouse = getattr(instance, spouse_field)
        if spouse:
            if not getattr(spouse, spouse_field) or getattr(spouse, spouse_field) == instance.person.refn:
                setattr(spouse, spouse_field, instance.person.refn)
                setattr(spouse, spouse_date, getattr(instance, spouse_date))
                setattr(spouse, spouse_place, getattr(instance, spouse_place))
                setattr(spouse, children_field, getattr(instance.person, children_field))
            elif getattr(spouse, next_spouse_field) in [None, '']:
                setattr(spouse, next_spouse_field, instance.person.refn)
            spouse.save()

            if spouse:
                for i in range(1, 5):
                    if not getattr(spouse, f'marr_spou_refn_{i}') or getattr(spouse, f'marr_spou_refn_{i}') == instance.person.refn:
                        setattr(spouse, f'marr_spou_refn_{i}', instance.person.refn)
                        setattr(spouse, f'marr_date_{i}', getattr(instance, spouse_date))
                        setattr(spouse, f'marr_plac_{i}', getattr(instance, spouse_place))
                        setattr(spouse, f'fam_chil_{i}', getattr(instance.person, children_field))
                        spouse.save()
                        break

    update_spouse('marr_spou_refn_1', 'marr_date_1', 'marr_plac_1', 'fam_chil_1', 'marr_spou_refn_2')
    update_spouse('marr_spou_refn_2', 'marr_date_2', 'marr_plac_2', 'fam_chil_2', 'marr_spou_refn_3')
    update_spouse('marr_spou_refn_3', 'marr_date_3', 'marr_plac_3', 'fam_chil_3', 'marr_spou_refn_4')
    update_spouse('marr_spou_refn_4', 'marr_date_4', 'marr_plac_4', 'fam_chil_4', None)


@receiver(post_save, sender=Relation)
def update_or_create_spouse_relation(sender, instance, created, **kwargs):
    if getattr(instance, '_updating', False):
        return

    spouse_fields_instance = [
        ('marr_spou_refn_1', 'marr_date_1', 'marr_plac_1'),
        ('marr_spou_refn_2', 'marr_date_2', 'marr_plac_2'),
        ('marr_spou_refn_3', 'marr_date_3', 'marr_plac_3'),
        ('marr_spou_refn_4', 'marr_date_4', 'marr_plac_4')
    ]

    for spou_refn_field, date_field, plac_field in spouse_fields_instance:
        spouse_refn = getattr(instance, spou_refn_field)
        if spouse_refn:
            spouse_relation, created = Relation.objects.get_or_create(person=spouse_refn)

            # Verhindere eine Endlosschleife
            spouse_relation._updating = True

            spouse_fields_spouse = [
                ('marr_spou_refn_1', 'marr_date_1', 'marr_plac_1'),
                ('marr_spou_refn_2', 'marr_date_2', 'marr_plac_2'),
                ('marr_spou_refn_3', 'marr_date_3', 'marr_plac_3'),
                ('marr_spou_refn_4', 'marr_date_4', 'marr_plac_4')
            ]

            # Durchlaufe die Felder beim Ehepartner, um das entsprechende Datum und den Ort zu setzen
            for spou_refn_field_spouse, date_field_spouse, plac_field_spouse in spouse_fields_spouse:
                if getattr(spouse_relation, spou_refn_field_spouse) == instance.person:
                    if getattr(instance, date_field):
                        setattr(spouse_relation, date_field_spouse, getattr(instance, date_field))
                    if getattr(instance, plac_field):
                        setattr(spouse_relation, plac_field_spouse, getattr(instance, plac_field))
                    break
                elif not getattr(spouse_relation, spou_refn_field_spouse):
                    setattr(spouse_relation, spou_refn_field_spouse, instance.person)
                    setattr(spouse_relation, date_field_spouse, getattr(instance, date_field))
                    setattr(spouse_relation, plac_field_spouse, getattr(instance, plac_field))
                    break

            spouse_relation.save()
            spouse_relation._updating = False


@receiver(m2m_changed, sender=Relation.children_1.through)
def update_or_create_child_relation(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        for child_id in pk_set:
            child = Person.objects.get(pk=child_id)
            relation, created = Relation.objects.get_or_create(person=child)

            # Verhindere Endlosschleifen
            relation._updating = True

            if instance.person.sex == 'F':
                relation.moth_refn = instance.person
            elif instance.person.sex == 'M':
                relation.fath_refn = instance.person
            else:
                # Wenn das Geschlecht 'D' ist oder nicht angegeben, finde eine freie Stelle
                if not relation.fath_refn:
                    relation.fath_refn = instance.person
                elif not relation.moth_refn:
                    relation.moth_refn = instance.person

            relation.save()
            relation._updating = False


@receiver(post_save, sender=Relation)
def update_parent_relations(sender, instance, **kwargs):
    # Verhindere Endlosschleifen
    if getattr(instance, '_updating', False):
        return

    # Logik für Mutter (moth_refn)
    if instance.moth_refn:
        mother_relation, created = Relation.objects.get_or_create(person=instance.moth_refn)
        mother_relation._updating = True

        # Finde den passenden Ehemann (fath_refn)
        if mother_relation.marr_spou_refn_1 is None or mother_relation.marr_spou_refn_1 == instance.fath_refn:
            mother_relation.marr_spou_refn_1 = instance.fath_refn
            mother_relation.children_1.add(instance.person)
        elif mother_relation.marr_spou_refn_2 is None or mother_relation.marr_spou_refn_2 == instance.fath_refn:
            mother_relation.marr_spou_refn_2 = instance.fath_refn
            mother_relation.children_2.add(instance.person)
        elif mother_relation.marr_spou_refn_3 is None or mother_relation.marr_spou_refn_3 == instance.fath_refn:
            mother_relation.marr_spou_refn_3 = instance.fath_refn
            mother_relation.children_3.add(instance.person)
        elif mother_relation.marr_spou_refn_4 is None or mother_relation.marr_spou_refn_4 == instance.fath_refn:
            mother_relation.marr_spou_refn_4 = instance.fath_refn
            mother_relation.children_4.add(instance.person)

        mother_relation.save()
        mother_relation._updating = False

    # Logik für Vater (fath_refn)
    if instance.fath_refn:
        father_relation, created = Relation.objects.get_or_create(person=instance.fath_refn)
        father_relation._updating = True

        # Finde die passende Ehefrau (moth_refn)
        if father_relation.marr_spou_refn_1 is None or father_relation.marr_spou_refn_1 == instance.moth_refn:
            father_relation.marr_spou_refn_1 = instance.moth_refn
            father_relation.children_1.add(instance.person)
        elif father_relation.marr_spou_refn_2 is None or father_relation.marr_spou_refn_2 == instance.moth_refn:
            father_relation.marr_spou_refn_2 = instance.moth_refn
            father_relation.children_2.add(instance.person)
        elif father_relation.marr_spou_refn_3 is None or father_relation.marr_spou_refn_3 == instance.moth_refn:
            father_relation.marr_spou_refn_3 = instance.moth_refn
            father_relation.children_3.add(instance.person)
        elif father_relation.marr_spou_refn_4 is None or father_relation.marr_spou_refn_4 == instance.moth_refn:
            father_relation.marr_spou_refn_4 = instance.moth_refn
            father_relation.children_4.add(instance.person)

        father_relation.save()
        father_relation._updating = False
