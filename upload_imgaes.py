import os
import shutil
from django.core.files import File

from django.conf import settings

from ancestors.models import Person

def migrate_files():
    media_root = settings.MEDIA_ROOT
    # Erstelle den Zielordner, falls er nicht existiert
    target_folder = os.path.join(media_root, 'images')
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for person in Person.objects.all():
        if person.obje_file_1:
            old_path = person.obje_file_1
            new_name = os.path.basename(old_path)
            new_path = os.path.join('images', new_name)
            
            # Kopiere die Datei in den Medienordner
            try:
                shutil.copy(old_path, os.path.join(media_root, new_path))
                # Setze den neuen Dateipfad
                person.obje_file_1.name = new_path
                person.save()
            except FileNotFoundError:
                print(f"Datei nicht gefunden: {old_path}")

migrate_files()
