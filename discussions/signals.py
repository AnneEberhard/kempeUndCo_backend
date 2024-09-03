import os
from django.db.models.signals import post_delete
from django.dispatch import receiver

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
