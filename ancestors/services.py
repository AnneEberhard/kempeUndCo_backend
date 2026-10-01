# services/relations.py

from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Person, Relation


def get_or_create_relation(person):

    relation, created = Relation.objects.get_or_create(
        person=person
    )

    return relation

def add_child_to_relationship(parent, other_parent, child):
    relation = get_or_create_relation(parent)

    # Nur ein Elternteil bekannt
    if other_parent is None:
        for index in range(1, 5):
            children = getattr(
                relation,
                f"children_{index}"
            )

            if not children.exists():
                children.add(child)
                return

        raise ValidationError(
            f"{parent.refn} hat keine freie Familienbeziehung mehr."
        )

    # Beide Eltern bekannt
    spouse_slot = None

    for index in range(1, 5):
        field = f"marr_spou_refn_{index}"

        if getattr(relation, field) == other_parent:
            spouse_slot = index
            break

    if spouse_slot is None:
        spouse_slot = ensure_spouse_slot(
            person=parent,
            spouse=other_parent,
        )

    children = getattr(
        relation,
        f"children_{spouse_slot}"
    )

    children.add(child)

def remove_child_from_relationship(parent, other_parent, child):
    """
    Entfernt child aus dem children_X-Slot der Beziehung
    zwischen parent und other_parent.
    """
    relation = Relation.objects.filter(
        person=parent
    ).first()

    if not relation:
        return

    # Nur ein Elternteil bekannt:
    # Kind aus allen children_X entfernen.
    if other_parent is None:
        for index in range(1, 5):
            children = getattr(
                relation,
                f"children_{index}"
            )

            if children.filter(pk=child.pk).exists():
                children.remove(child)

        return

    # Beide Eltern bekannt:
    # passenden Beziehungsslot suchen.

    for index in range(1, 5):
        spouse_field = f"marr_spou_refn_{index}"

        if getattr(relation, spouse_field) == other_parent:
            children = getattr(
                relation,
                f"children_{index}"
            )

            if children.filter(pk=child.pk).exists():
                children.remove(child)
   

def remove_child_from_parent(parent, child):
    """
    Entfernt child aus allen children_X-Feldern
    der Relation von parent.
    """

    relation = Relation.objects.filter(
        person=parent
    ).first()

    if not relation:
        return

    for index in range(1, 5):
        children = getattr(
            relation,
            f"children_{index}"
        )

        if children.filter(pk=child.pk).exists():
            children.remove(child)

def remove_parent_from_child(parent, child):
    """
    Entfernt parent als Vater oder Mutter von child
    und synchronisiert die inverse children_X-Beziehung.
    """

    child_relation = get_or_create_relation(child)
    print(
        "REMOVE PARENT CALLED:",
        "parent =", parent.refn,
        "child =", child.refn,
        "father =", (
            child_relation.fath_refn.refn
            if child_relation.fath_refn
            else None
        ),
        "mother =", (
            child_relation.moth_refn.refn
            if child_relation.moth_refn
            else None
        ),
    )

    if child_relation.fath_refn == parent:
        print(
    "REMOVE PARENT:",
    "parent =", parent.refn,
    "child =", child.refn,
    "father =", (
        child_relation.fath_refn.refn
        if child_relation.fath_refn
        else None
    ),
    "mother =", (
        child_relation.moth_refn.refn
        if child_relation.moth_refn
        else None
    ),
)
        other_parent = child_relation.moth_refn

        child_relation.fath_refn = None
        child_relation.save(
            update_fields=["fath_refn"]
        )

    elif child_relation.moth_refn == parent:
        print(
            "REMOVE PARENT:",
            "parent =", parent.refn,
            "child =", child.refn,
            "father =", (
                child_relation.fath_refn.refn
                if child_relation.fath_refn
                else None
            ),
            "mother =", (
                child_relation.moth_refn.refn
                if child_relation.moth_refn
                else None
            ),
        )
        
        other_parent = child_relation.fath_refn

        child_relation.moth_refn = None
        child_relation.save(
            update_fields=["moth_refn"]
        )

    else:
        return

def add_spouse(person, spouse, preferred_slot=None):
    """
    Stellt sicher, dass spouse in einer marr_spou_refn_X-
    Relation von person eingetragen ist.

    preferred_slot wird bevorzugt verwendet.
    """
    relation = get_or_create_relation(person)

    # Bereits vorhanden?
    for index in range(1, 5):
        existing_spouse = getattr(
            relation,
            f"marr_spou_refn_{index}"
        )

        if existing_spouse == spouse:
            return

    # Bevorzugten Slot versuchen
    if preferred_slot:
        field = f"marr_spou_refn_{preferred_slot}"

        if getattr(relation, field) is None:
            setattr(relation, field, spouse)
            relation.save(update_fields=[field])
            return

    # Ersten freien Slot suchen
    for index in range(1, 5):
        field = f"marr_spou_refn_{index}"

        if getattr(relation, field) is None:
            setattr(relation, field, spouse)
            relation.save(update_fields=[field])
            return

    raise ValidationError(
        f"{person.refn} hat bereits 4 Ehepartner eingetragen."
    )

def remove_spouse(person, spouse):
    """
    Entfernt spouse aus allen marr_spou_refn_X-Feldern
    der Relation von person.
    """
    relation = Relation.objects.filter(
        person=person
    ).first()

    if not relation:
        return

    fields_to_update = []

    for index in range(1, 5):
        field = f"marr_spou_refn_{index}"
        existing_spouse = getattr(relation, field)

        if existing_spouse == spouse:
            setattr(relation, field, None)
            fields_to_update.append(field)

            for field in (
                f"marr_date_{index}",
                f"marr_plac_{index}",
                f"fam_stat_{index}",
            ):
                setattr(relation, field, None)
                fields_to_update.append(field)

    if fields_to_update:
        relation.save(update_fields=fields_to_update)

def ensure_spouse_slot(person, spouse):
    """
    Sucht den Slot, in dem spouse bei person eingetragen ist.

    Falls spouse noch nicht eingetragen ist, wird der erste
    freie marr_spou_refn_X-Slot verwendet.

    Gibt die Slot-Nummer (1-4) zurück.
    """

    relation = get_or_create_relation(person)

    # Existierende Beziehung suchen
    for index in range(1, 5):
        field = f"marr_spou_refn_{index}"

        if getattr(relation, field) == spouse:
            return index

    # Freien Slot suchen
    for index in range(1, 5):
        field = f"marr_spou_refn_{index}"

        if getattr(relation, field) is None:
            setattr(relation, field, spouse)
            relation.save(update_fields=[field])
            return index

    raise ValidationError(
        f"{person.refn} hat bereits 4 Beziehungen."
    )

def sync_child_from_parent(parent, child):
    """
    Synchronisiert eine direkte children_X-Zuordnung
    mit der Elternstruktur des Kindes.
    """

    child_relation = get_or_create_relation(child)
    # Elternrolle bestimmen
    if parent.sex == "M":
        old_parent = child_relation.fath_refn
        
        if old_parent and old_parent != parent:
            print("sync child: ", child.refn)
            print("sync parent: ", parent.refn)
            remove_parent_from_child(
                parent=old_parent,
                child=child,
            )

        child_relation.fath_refn = parent
        child_relation.save(update_fields=["fath_refn"])
        print("child_relation.moth_refn: ", child_relation.moth_refn)
        other_parent = child_relation.moth_refn

    elif parent.sex == "F":

        old_parent = child_relation.moth_refn
        if old_parent and old_parent != parent:

            remove_parent_from_child(
                parent=old_parent,
                child=child,
            )

        child_relation.moth_refn = parent
        child_relation.save(update_fields=["moth_refn"])

        other_parent = child_relation.fath_refn

    else:
        raise ValidationError(
            f"Die Elternrolle von {parent.refn} kann nicht "
            f"automatisch bestimmt werden."
        )

    # Anderen Elternteil ebenfalls synchronisieren
    if other_parent:
        print("sync other: ", other_parent.refn)
        add_child_to_relationship(
            parent=parent,
            other_parent=other_parent,
            child=child,
        )

        add_child_to_relationship(
            parent=other_parent,
            other_parent=parent,
            child=child,
        )

def sync_spouse_data(
    person,
    spouse,
    marr_date=None,
    marr_plac=None,
    fam_stat=None
):
    """
    Spiegelt Heiratsdatum und Heiratsort einer Partnerschaft
    auf den entsprechenden Partnerschafts-Slot des anderen Partners.
    """

    relation = get_or_create_relation(spouse)

    # Bestehenden Slot des Partners suchen
    spouse_slot = None

    for index in range(1, 5):
        field = f"marr_spou_refn_{index}"

        if getattr(relation, field) == person:
            spouse_slot = index
            break

    # Falls die Partnerschaft noch nicht existiert,
    # freien Slot verwenden.
    if spouse_slot is None:
        spouse_slot = ensure_spouse_slot(
            person=spouse,
            spouse=person,
        )

    date_field = f"marr_date_{spouse_slot}"
    plac_field = f"marr_plac_{spouse_slot}"
    stat_field = f"fam_stat_{spouse_slot}"

    setattr(relation, date_field, marr_date)
    setattr(relation, plac_field, marr_plac)
    setattr(relation, stat_field, fam_stat)

    relation.save(
        update_fields=[
            date_field,
            plac_field,
            stat_field
        ]
    )

def sync_person_legacy_fields(person):
    """
    Spiegelt die Daten aus Relation in die alten Person-Felder.

    Relation ist die Quelle. Es findet hier keine
    Beziehungs-Synchronisation statt.
    """

    relation = get_or_create_relation(person)
    print("update für Person: ", person.refn)

    # Eltern
    person.fath_refn = (
        relation.fath_refn.refn
        if relation.fath_refn
        else None
    )

    person.fath_name = (
        relation.fath_refn.name
        if relation.fath_refn
        else None
    )

    person.moth_refn = (
        relation.moth_refn.refn
        if relation.moth_refn
        else None
    )

    person.moth_name = (
        relation.moth_refn.name
        if relation.moth_refn
        else None
    )

    # Partnerschaften
    for index in range(1, 5):

        spouse = getattr(
            relation,
            f"marr_spou_refn_{index}"
        )

        # Partner
        setattr(
            person,
            f"marr_spou_refn_{index}",
            spouse.refn if spouse else None,
        )

        setattr(
            person,
            f"marr_spou_name_{index}",
            spouse.name if spouse else None,
        )

        # Heiratsdaten
        setattr(
            person,
            f"marr_date_{index}",
            getattr(
                relation,
                f"marr_date_{index}"
            ),
        )

        setattr(
            person,
            f"marr_plac_{index}",
            getattr(
                relation,
                f"marr_plac_{index}"
            ),
        )

        # Familienstand
        setattr(
            person,
            f"fam_stat_{index}",
            getattr(
                relation,
                f"fam_stat_{index}"
            ),
        )

        # Kinder
        children = getattr(
            relation,
            f"children_{index}"
        ).all()

        child_refns = [
            child.refn
            for child in children
        ]

        setattr(
            person,
            f"fam_chil_{index}",
            ", ".join(child_refns) if child_refns else None,
        )

    person.save()