import os
import django
from django.conf import settings
from django.core.files.storage import default_storage

# Django Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kempeUndCo_backend.settings')
django.setup()

from ancestors.models import Person


def rename_and_update_paths():
    for person in Person.objects.all():
        for i in range(1, 7):
            field_name = f'obje_file_{i}'
            file_field = getattr(person, field_name)

            if file_field and file_field.name:
                old_path = file_field.path
                # Neuer Name basierend auf der ID und dem Feldindex
                new_filename = f"{person.id}_image{i}{os.path.splitext(old_path)[1]}"
                new_path = os.path.join('images/', new_filename)

                # Pfad innerhalb des MEDIA_ROOT anpassen
                new_full_path = os.path.join(settings.MEDIA_ROOT, new_path)

                # Datei umbenennen
                if os.path.exists(old_path):
                    os.rename(old_path, new_full_path)

                    # Pfad im Datenbankfeld aktualisieren
                    file_field.name = new_path
                    person.save()
                    print(f"Renamed {old_path} to {new_full_path}")


if __name__ == "__main__":
    rename_and_update_paths()
