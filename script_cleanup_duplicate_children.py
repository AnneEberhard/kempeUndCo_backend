import os
import django
from django.db.models import Q

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kempeUndCo_backend.settings')
django.setup()

from ancestors.models import Person, Relation

def cleanup_duplicate_children():
    relations = Relation.objects.all()
    updated_count = 0

    for relation in relations:
        # Abrufen der Kinder-IDs aus den verschiedenen Ehen
        children_lists = {
            'children_1': set(relation.children_1.values_list('id', flat=True)),
            'children_2': set(relation.children_2.values_list('id', flat=True)),
            'children_3': set(relation.children_3.values_list('id', flat=True)),
            'children_4': set(relation.children_4.values_list('id', flat=True))
        }

        # Erstellen eines Sets von bereits gesehenen Gruppen von Kindern
        seen_children_groups = []
        duplicates_found = False

        # Überprüfung auf Duplikate
        for key, children_ids in children_lists.items():
            children_ids_sorted = tuple(sorted(children_ids))
            if children_ids_sorted in seen_children_groups:
                # Wenn diese Gruppe von Kindern bereits gesehen wurde, markiere als Duplikat
                getattr(relation, key).clear()  # Leeren der Many-to-Many-Beziehung
                duplicates_found = True
            else:
                seen_children_groups.append(children_ids_sorted)

        if duplicates_found:
            # Stelle sicher, dass die verbleibenden Listen von Kindern nur einmalig enthalten sind
            for key, children_ids in children_lists.items():
                children_ids_sorted = tuple(sorted(children_ids))
                if children_ids_sorted in seen_children_groups:
                    # Setze die korrekten Kinder-IDs
                    getattr(relation, key).set(Person.objects.filter(id__in=children_ids_sorted))
                    seen_children_groups.remove(children_ids_sorted)
                else:
                    # Leere die nicht mehr benötigten Kinder-IDs
                    getattr(relation, key).clear()

            # Speichere die Änderungen
            relation.save()
            updated_count += 1

    print(f"Updated {updated_count} Relation records with unique children data.")

if __name__ == "__main__":
    cleanup_duplicate_children()
