from import_export import resources
from django.utils.dateparse import parse_datetime
from django.utils import timezone


class TimestampRestoreResource(resources.ModelResource):

    def after_save_instance(self, instance, row, **kwargs):
        created_at = row.get("created_at")
        updated_at = row.get("updated_at")

        if created_at:
            dt = parse_datetime(created_at)
            if dt and timezone.is_naive(dt):
                dt = timezone.make_aware(dt, timezone.utc)

            type(instance).objects.filter(pk=instance.pk).update(
                created_at=dt
            )

        if updated_at:
            dt = parse_datetime(updated_at)

            if dt and timezone.is_naive(dt):
                dt = timezone.make_aware(dt, timezone.utc)

            type(instance).objects.filter(pk=instance.pk).update(
                updated_at=dt
            )