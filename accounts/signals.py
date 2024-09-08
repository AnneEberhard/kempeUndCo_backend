from django.db.models.signals import post_save
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from .models import CustomUser
from django.contrib.contenttypes.models import ContentType
from recipes.models import Recipe
from infos.models import Info
from comments.models import Comment
from discussions.models import DiscussionEntry, Discussion
from accounts.models import CustomUser
from ancestors.models import Relation, Person


@receiver(post_save, sender=CustomUser)
def set_default_staff_permissions(sender, instance, created, **kwargs):
    if instance.is_staff and not instance.is_superuser:
        model_permissions = [
            ('add_recipe', 'Can add recipe', Recipe),
            ('change_recipe', 'Can change recipe', Recipe),
            ('delete_recipe', 'Can delete recipe', Recipe),
            ('view_recipe', 'Can view recipe', Recipe),
            ('add_info', 'Can add info', Info),
            ('change_info', 'Can change info', Info),
            ('delete_info', 'Can delete info', Info),
            ('view_info', 'Can view info', Info),
            ('add_comment', 'Can add comment', Comment),
            ('change_comment', 'Can change comment', Comment),
            ('delete_comment', 'Can delete comment', Comment),
            ('view_comment', 'Can view comment', Comment),
            ('add_discussionentry', 'Can add discussion entry', DiscussionEntry),
            ('change_discussionentry', 'Can change discussion entry', DiscussionEntry),
            ('delete_discussionentry', 'Can delete discussion entry', DiscussionEntry),
            ('view_discussionentry', 'Can view discussion entry', DiscussionEntry),
            ('add_discussion', 'Can add discussion', Discussion),
            ('change_discussion', 'Can change discussion', Discussion),
            ('view_discussion', 'Can view discussion', Discussion),
            ('add_customuser', 'Can add user', CustomUser),
            ('change_customuser', 'Can change user', CustomUser),
            ('view_customuser', 'Can view user', CustomUser),
            ('add_relation', 'Can add relation', Relation),
            ('change_relation', 'Can change relation', Relation),
            ('view_relation', 'Can view relation', Relation),
            ('add_person', 'Can add person', Person),
            ('change_person', 'Can change person', Person),
            ('view_person', 'Can view person', Person),
        ]

        for codename, name, model_class in model_permissions:
            content_type = ContentType.objects.get_for_model(model_class)
            permission, created = Permission.objects.get_or_create(
                codename=codename,
                content_type=content_type,
                defaults={
                    "name": name,
                }
            )
            if permission not in instance.user_permissions.all():
                instance.user_permissions.add(permission)
    elif not instance.is_superuser:
        # Clear permissions only if the user is not a superuser
        instance.user_permissions.clear()



# @receiver(post_save, sender=CustomUser)
# def assign_user_to_groups(sender, instance, created, **kwargs):
#     global processing_signal
# 
#     if not processing_signal:
#         processing_signal = True
# 
#         # Lösche alle bestehenden Gruppenmitgliedschaften
#         instance.groups.clear()
# 
#         # Bestimme die Gruppen basierend auf den family_-Werten
#         families = {instance.family_1, instance.family_2}
# 
#         for family in families:
#             if family:
#                 group_name = f"Stammbaum {family.capitalize()}"
#                 group, created = Group.objects.get_or_create(name=group_name)
#                 instance.groups.add(group)
# 
#         processing_signal = True
#         instance.save()
#         processing_signal = False
