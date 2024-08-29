import os
import django

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kempeUndCo_backend.settings')
django.setup()

from ancestors.models import Person


def update_family_trees():
    # Setzt family_1 auf 'kempe' für alle Datensätze
    persons = Person.objects.all()
    updated_count = 0
    for person in persons:
        if person.family_1 != 'kempe':
            person.family_1 = 'kempe'
            person.save()
            updated_count += 1
    print(f"Updated {updated_count} records to family_1='kempe'.")


if __name__ == "__main__":
    update_family_trees()
