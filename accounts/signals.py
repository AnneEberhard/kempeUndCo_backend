from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from .models import CustomUser

# Ein Flag, um zu verhindern, dass save() innerhalb des Signals erneut aufgerufen wird
processing_signal = False


@receiver(post_save, sender=CustomUser)
def assign_user_to_groups(sender, instance, created, **kwargs):
    global processing_signal

    if not processing_signal:
        processing_signal = True

        # Lösche alle bestehenden Gruppenmitgliedschaften
        instance.groups.clear()

        # Bestimme die Gruppen basierend auf den family_-Werten
        families = {instance.family_1, instance.family_2}

        for family in families:
            if family:
                group_name = f"Stammbaum {family.capitalize()}"
                group, created = Group.objects.get_or_create(name=group_name)
                instance.groups.add(group)

        # Kein erneutes Speichern des Benutzers nötig
        processing_signal = False
