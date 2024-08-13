import os
import django
from django.db.models import Q

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kempeUndCo_backend.settings')
django.setup()

from ancestors.models import Person, Relation


def migrate_children_to_related_data():
    persons = Person.objects.all()
    updated_count = 0

    for person in persons:
        related_data, created = Relation.objects.get_or_create(person=person)
        updated = False

        # Kinder aus Ehe 1
        children_1 = Person.objects.filter(
            (Q(fath_refn=person.refn) & Q(moth_refn=person.marr_spou_refn_1)) | (Q(fath_refn=person.marr_spou_refn_1) & Q(moth_refn=person.refn))
        )
        if children_1.exists():
            related_data.children_1.set(children_1)
            updated = True

        # Kinder aus Ehe 2
        children_2 = Person.objects.filter(
            (Q(fath_refn=person.refn) & Q(moth_refn=person.marr_spou_refn_2)) | (Q(fath_refn=person.marr_spou_refn_2) & Q(moth_refn=person.refn))
        )
        if children_2.exists():
            related_data.children_2.set(children_2)
            updated = True

        # Kinder aus Ehe 3
        children_3 = Person.objects.filter(
            (Q(fath_refn=person.refn) & Q(moth_refn=person.marr_spou_refn_3)) | (Q(fath_refn=person.marr_spou_refn_3) & Q(moth_refn=person.refn))
        )
        if children_3.exists():
            related_data.children_3.set(children_3)
            updated = True

        # Kinder aus Ehe 4
        children_4 = Person.objects.filter(
            (Q(fath_refn=person.refn) & Q(moth_refn=person.marr_spou_refn_4)) | (Q(fath_refn=person.marr_spou_refn_4) & Q(moth_refn=person.refn))
        )
        if children_4.exists():
            related_data.children_4.set(children_4)
            updated = True

        if updated:
            related_data.save()
            updated_count += 1

    print(f"Updated {updated_count} records with children data.")


if __name__ == "__main__":
    migrate_children_to_related_data()
