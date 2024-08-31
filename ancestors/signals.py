import os
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save

from .tasks import rename_image
from .models import Person


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
