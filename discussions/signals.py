import os
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from kempeUndCo_backend.settings import EMAIL_HOST_USER

from .models import DiscussionEntry


@receiver(post_delete, sender=DiscussionEntry)
def delete_images_on_entry_delete(sender, instance, **kwargs):
    """
    Deletes associated image files and thumbnails when a discussion entry instance is deleted.
    """
    for field in ['image_1', 'image_2', 'image_3', 'image_4']:
        image = getattr(instance, field)
        if image and os.path.isfile(image.path):
            os.remove(image.path)

        thumbnail_field = f'{field}_thumbnail'
        thumbnail = getattr(instance, thumbnail_field)
        if thumbnail and os.path.isfile(thumbnail.path):
            os.remove(thumbnail.path)


@receiver(post_delete, sender=DiscussionEntry)
def delete_empty_discussion(sender, instance, **kwargs):
    """
    Signal handler to delete the associated discussion if it has no more entries.
    Triggered after a DiscussionEntry is deleted.
    """
    discussion = instance.discussion
    if not discussion.entries.exists():  # Check if there are no more entries
        discussion.delete()  # Delete the discussion if it's empty


@receiver(post_save, sender=DiscussionEntry)
def notify_new_discussion(sender, instance, created, **kwargs):
    if created:
        
        print(instance.discussion.person.name)
        send_mail(
            'Neuer Diskussionsbeitrag erstellt',
            f'Es wurde ein neuer Diskussionsbeitrag zu Person "{instance.discussion.person.name}" auf der Webseite KempeUndCo erstellt.',
            settings.DEFAULT_FROM_EMAIL,
            [EMAIL_HOST_USER],
            fail_silently=False,
        )
