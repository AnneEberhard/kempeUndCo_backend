import os
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save

from .tasks import rename_image
from .models import Person


@receiver(post_save, sender=Person)
def rename_files_on_save(sender, instance, created, **kwargs):
    if not hasattr(instance, '_performing_post_save'):
        instance._performing_post_save = False

    if not instance._performing_post_save:
        instance._performing_post_save = True

        for i in range(1, 7):
            field_name = f'obje_file_{i}'
            file_field = getattr(instance, field_name)

            if file_field and file_field.name:
                # Alter Dateiname
                old_path = file_field.path
                # Neuer Dateiname
                new_path = rename_image(instance, file_field.name, i)
                # Pfad innerhalb des MEDIA_ROOT
                new_full_path = os.path.join(settings.MEDIA_ROOT, new_path)

                # Datei umbenennen
                if os.path.exists(old_path) and old_path != new_full_path:
                    os.rename(old_path, new_full_path)

                    # Pfad im Datenbankfeld aktualisieren
                    file_field.name = new_path

        instance.save(update_fields=[f'obje_file_{i}' for i in range(1, 7)])
        instance._performing_post_save = False


@receiver(pre_save, sender=Person)
def delete_old_files_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return False  # Beim Erstellen eines neuen Objekts gibt es nichts zu tun

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return False  # Das alte Objekt existiert nicht, nichts zu tun

    for i in range(1, 7):
        field_name = f'obje_file_{i}'
        old_file = getattr(old_instance, field_name)
        new_file = getattr(instance, field_name)

        if old_file and old_file != new_file:
            if os.path.exists(old_file.path):
                os.remove(old_file.path)


@receiver(post_delete, sender=Person)
def delete_files_on_delete(sender, instance, **kwargs):
    for i in range(1, 7):
        field_name = f'obje_file_{i}'
        file_field = getattr(instance, field_name)
        if file_field and file_field.name:
            file_path = file_field.path
            if os.path.exists(file_path):
                os.remove(file_path)
