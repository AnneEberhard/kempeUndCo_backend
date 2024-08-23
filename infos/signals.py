import os
from django.db.models.signals import post_delete
from django.dispatch import receiver

from infos.models import Info

@receiver(post_delete, sender=Info)
def delete_images_on_info_delete(sender, instance, **kwargs):
    # Deletes images if they exist
    for field in ['image_1', 'image_2', 'image_3', 'image_4']:
        image = getattr(instance, field)
        if image and os.path.isfile(image.path):
            os.remove(image.path)
