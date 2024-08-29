from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from .models import CustomUser

# Ein Flag, um zu verhindern, dass save() innerhalb des Signals erneut aufgerufen wird
processing_signal = False

@receiver(post_save, sender=CustomUser)
def assign_user_to_groups(sender, instance, **kwargs):
    for group_name in ["Stammbaum Kempe", "Stammbaum Hünten"]:
        print(Group.objects.filter(name=group_name).exists())
    # Lösche alle bestehenden Gruppenmitgliedschaften
    print(f"pre: {instance.groups}")
    instance.groups.clear()
    print(f"cleared: {instance.groups}")

    # Bestimme die Gruppen basierend auf den family_-Werten
    families = {instance.family_1, instance.family_2}
    print(f"Zuordnen: {families}")

    for family in families:
        if family:
            group_name = f"Stammbaum {family.capitalize()}"
            print(f"Erstelle oder hole Gruppe: {group_name}")
            group, created = Group.objects.get_or_create(name=group_name)
            instance.groups.add(group)
            print(f"Gruppe hinzugefügt: {group.name}")

    # Kein erneutes Speichern des Benutzers nötig
    print(f"Benutzer-Gruppen nach dem Speichern: {[group.name for group in instance.groups.all()]}")