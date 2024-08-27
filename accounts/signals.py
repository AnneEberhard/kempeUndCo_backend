from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

from accounts.models import CustomUser


@receiver(post_save, sender=CustomUser)
def assign_new_user_to_groups(sender, instance, **kwargs):
    if kwargs.get('created', False):
        # Lösche alle bestehenden Gruppenmitgliedschaften
        instance.groups.clear()
        
        # Bestimme die Gruppen basierend auf den family_tree-Werten
        family_trees = {instance.family_tree_1, instance.family_tree_2}
        
        for tree in family_trees:
            if tree:
                group_name = f"Stammbaum {tree.capitalize()}"
                group, created = Group.objects.get_or_create(name=group_name)
                instance.groups.add(group)
