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