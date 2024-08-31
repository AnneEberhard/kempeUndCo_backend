import os
from django.db.models.signals import post_delete
from django.dispatch import receiver

from infos.models import Info


@receiver(post_delete, sender=Info)
def delete_images_on_info_delete(sender, instance, **kwargs):
    """
    Deletes associated image files when an Info instance is deleted.

    This signal handler is triggered after an Info instance is deleted. It iterates over the image fields
    (`image_1`, `image_2`, `image_3`, and `image_4`) and removes the image files from the filesystem if they exist.

    Args:
        sender (Model): The model class that sent the signal.
        instance (Info): The instance of Info that was deleted.
        **kwargs: Additional keyword arguments passed by the signal dispatcher.
    """
    for field in ['image_1', 'image_2', 'image_3', 'image_4']:
        image = getattr(instance, field)
        if image and os.path.isfile(image.path):
            os.remove(image.path)
