from ancestors.models import PersonChangeLog
import uuid


def log_person_changes(person, old_values, new_values, user):
    if not user:
        return

    change_id = uuid.uuid4()

    for field_name, old_value in old_values.items():

        if field_name not in new_values:
            continue

        new_value = new_values.get(field_name)

        if old_value != new_value:
            
            PersonChangeLog.objects.create(
                change_id=change_id,
                person=person,
                changed_by=user,
                field_name=field_name,
                old_value='' if old_value is None else str(old_value),
                new_value='' if new_value is None else str(new_value),
            )

def log_relation_changes(relation, old_values, new_values, requested_fields, user):
    if not user:
        return

    change_id = uuid.uuid4()

    for field_name in old_values:

        # Nur Felder berücksichtigen,
        # die tatsächlich vom Frontend geschickt wurden.
        if field_name not in requested_fields:
            continue

        old_value = old_values[field_name]
        new_value = new_values[field_name]

        if old_value == new_value:
            continue

        PersonChangeLog.objects.create(
            change_id=change_id,
            person=relation.person,
            changed_by=user,
            field_name=f'relation.{field_name}',
            old_value=old_value,
            new_value=new_value,
        )

def get_relation_field_value(relation, field_name):
    value = getattr(relation, field_name)

    if field_name.startswith('children_'):
        return ', '.join(
            value.order_by('refn').values_list('refn', flat=True)
        )

    if field_name.startswith('marr_spou_refn_') or field_name in (
        'fath_refn',
        'moth_refn',
    ):
        return value.refn if value else ''

    return '' if value is None else str(value)
