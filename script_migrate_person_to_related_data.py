import os
import django

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kempeUndCo_backend.settings')
django.setup()

from ancestors.models import Person, Relation


def migrate_person_to_related_data():
    persons = Person.objects.all()
    created_count = 0

    for person in persons:
        related_data, created = Relation.objects.get_or_create(person=person)
        updated = False

        if person.fath_refn and isinstance(person.fath_refn, str):
            father = Person.objects.filter(refn=person.fath_refn).first()
            if father:
                related_data.fath_refn = father
                updated = True

        if person.moth_refn and isinstance(person.moth_refn, str):
            mother = Person.objects.filter(refn=person.moth_refn).first()
            if mother:
                related_data.moth_refn = mother
                updated = True

        if person.marr_spou_refn_1 and isinstance(person.marr_spou_refn_1, str):
            spouse1 = Person.objects.filter(refn=person.marr_spou_refn_1).first()
            if spouse1:
                related_data.marr_spou_refn_1 = spouse1
                updated = True

        if person.marr_spou_refn_2 and isinstance(person.marr_spou_refn_2, str):
            spouse2 = Person.objects.filter(refn=person.marr_spou_refn_2).first()
            if spouse2:
                related_data.marr_spou_refn_2 = spouse2
                updated = True

        if person.marr_spou_refn_3 and isinstance(person.marr_spou_refn_3, str):
            spouse3 = Person.objects.filter(refn=person.marr_spou_refn_3).first()
            if spouse3:
                related_data.marr_spou_refn_3 = spouse3
                updated = True

        if person.marr_spou_refn_4 and isinstance(person.marr_spou_refn_4, str):
            spouse4 = Person.objects.filter(refn=person.marr_spou_refn_4).first()
            if spouse4:
                related_data.marr_spou_refn_4 = spouse4
                updated = True

        if updated:
            related_data.save()
            created_count += 1

    print(f"Created and updated {created_count} RelatedData records.")


if __name__ == "__main__":
    migrate_person_to_related_data()
