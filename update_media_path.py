import os
import django
from django.conf import settings

# Setze die Django-Einstellungen
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kempeUndCo_backend.settings')
django.setup()


from ancestors.models import Person


def update_file_paths():
    media_root = settings.MEDIA_ROOT
    target_folder = 'images'

    # Liste der Felder, die aktualisiert werden sollen
    fields_to_update = ['obje_file_1', 'obje_file_2', 'obje_file_3', 'obje_file_4', 'obje_file_5', 'obje_file_6']

    for person in Person.objects.all():
        for field in fields_to_update:
            old_path = getattr(person, field)
            if old_path:
                new_name = os.path.basename(old_path)  # Nur den Dateinamen extrahieren
                new_path = os.path.join(target_folder, new_name)  # Den neuen Pfad erstellen

                # Setze den neuen Dateipfad ohne die Datei zu kopieren
                setattr(person, field, new_path)
        
        # Speichere die Änderungen des Person-Objekts
        person.save()

if __name__ == "__main__":
    update_file_paths()
