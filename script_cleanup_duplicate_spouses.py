import os
import django

# Django-Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kempeUndCo_backend.settings')
django.setup()

from ancestors.models import Relation

def cleanup_duplicate_spouses():
    # Hole alle Relation-Objekte
    relations = Relation.objects.all()

    updated_count = 0

    for relation in relations:
        updated = False
        
        # Überprüfen und Bereinigen der Ehepartner-Referenzen
        if relation.marr_spou_refn_2 == relation.marr_spou_refn_1:
            relation.marr_spou_refn_2 = None
            updated = True
        if relation.marr_spou_refn_3 == relation.marr_spou_refn_1:
            relation.marr_spou_refn_3 = None
            updated = True
        if relation.marr_spou_refn_4 == relation.marr_spou_refn_1:
            relation.marr_spou_refn_4 = None
            updated = True
        
        # Speichern der Änderungen, wenn Änderungen vorgenommen wurden
        if updated:
            relation.save()
            updated_count += 1
            print(f'Updated relation for person: {relation.person.refn}')

    print(f'Updated {updated_count} Relation records.')

if __name__ == "__main__":
    cleanup_duplicate_spouses()
