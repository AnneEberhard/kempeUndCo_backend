import os
from django.db.models.signals import post_delete
from django.dispatch import receiver

from recipes.models import Recipe

@receiver(post_delete, sender=Recipe)
def delete_images_on_recipe_delete(sender, instance, **kwargs):
    # Deletes images if they exist
    for field in ['image_1', 'image_2', 'image_3', 'image_4']:
        image = getattr(instance, field)
        if image and os.path.isfile(image.path):
            os.remove(image.path)
