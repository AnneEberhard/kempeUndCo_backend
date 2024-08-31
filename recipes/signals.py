import os
from django.db.models.signals import post_delete
from django.dispatch import receiver

from recipes.models import Recipe

@receiver(post_delete, sender=Recipe)
def delete_images_on_recipe_delete(sender, instance, **kwargs):
    """
    Signal handler for the `post_delete` signal of the `Recipe` model.

    This function is called after a `Recipe` instance is deleted. It ensures that any associated 
    images stored on the filesystem are also deleted. It checks each image field (`image_1`, 
    `image_2`, `image_3`, `image_4`) and removes the file if it exists.

    **Parameters:**
    - `sender`: The model class that sent the signal (i.e., `Recipe`).
    - `instance`: The instance of the model that was deleted.

    **Process:**
    - Iterates over the image fields of the `Recipe` model.
    - For each field, checks if the image exists and if the file path is valid.
    - If the file exists, deletes it from the filesystem.

    **Usage:**
    This function helps to avoid orphaned image files on the server when a `Recipe` is deleted.

    **Note:**
    - This function assumes that the image fields store files that are managed by Django's 
      `FileField` and that the files are stored on the filesystem.
    """
    for field in ['image_1', 'image_2', 'image_3', 'image_4']:
        image = getattr(instance, field)
        if image and os.path.isfile(image.path):
            os.remove(image.path)
