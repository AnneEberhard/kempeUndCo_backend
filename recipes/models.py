import os
from django.db import models
from django.conf import settings
from kempeUndCo_backend.constants import FAMILY_CHOICES
from utils.html_cleaner import clean_html
from PIL import Image
import io
from django.core.files.base import ContentFile


class Recipe(models.Model):
    """
    Represents a recipe in the system.

    **Fields:**
    - `title`: The title of the recipe.
    - `content`: The content or instructions for the recipe.
    - `author`: The user who created the recipe (ForeignKey to the user model).
    - `created_at`: The timestamp when the recipe was created (auto-populated).
    - `updated_at`: The timestamp when the recipe was last updated (auto-populated).
    - `image_1`: The first image associated with the recipe.
    - `image_2`: The second image associated with the recipe.
    - `image_3`: The third image associated with the recipe.
    - `image_4`: The fourth image associated with the recipe.
    - `family_1`: The first family tree associated with the recipe.
    - `family_2`: The second family tree associated with the recipe.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Image fields with custom upload paths
    image_1 = models.FileField(upload_to='recipes/', null=True, blank=True)
    image_2 = models.FileField(upload_to='recipes/', null=True, blank=True)
    image_3 = models.FileField(upload_to='recipes/', null=True, blank=True)
    image_4 = models.FileField(upload_to='recipes/', null=True, blank=True)

    family_1 = models.CharField(choices=FAMILY_CHOICES, max_length=50, blank=True, verbose_name='Stammbaum 1')
    family_2 = models.CharField(choices=FAMILY_CHOICES, max_length=50, blank=True, null=True, verbose_name='Stammbaum 2')

    def compress_image(self, image_file):
        """
        Compresses an image and returns it as a ContentFile.
        """
        if not image_file:
            return image_file

        img = Image.open(image_file)
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=70)
        output.seek(0)
        return ContentFile(output.read(), image_file.name)

    def save(self, *args, **kwargs):
        """
        Save the recipe instance.

        Cleans the HTML content using `clean_html`, and handles deletion of old images
        if they have been replaced with new ones.

        **Parameters:**
        - `*args`: Variable length argument list.
        - `**kwargs`: Keyword arguments.

        **Behavior:**
        - If the recipe instance already exists (i.e., it is being updated), it checks
          if any old images are being replaced by new ones. If so, it deletes the old images
          from the filesystem.

        **Notes:**
        - The `clean_html` function is used to sanitize the content field before saving.
        """
        self.content = clean_html(self.content)

        for i in range(1, 5):
            image_field = getattr(self, f'image_{i}')
            if image_field and hasattr(image_field, 'file'):
                # Komprimiere das Bild
                compressed_image = self.compress_image(image_field.file)
                setattr(self, f'image_{i}', compressed_image)

        if self.pk:  # Only if instance already exists
            old_recipe = Recipe.objects.get(pk=self.pk)
            for i in range(1, 5):
                old_image = getattr(old_recipe, f'image_{i}')
                new_image = getattr(self, f'image_{i}')
                if old_image and old_image != new_image:
                    if os.path.isfile(old_image.path):
                        os.remove(old_image.path)

        super().save(*args, **kwargs)

    def __str__(self):
        """
        Return a string representation of the recipe.

        **Returns:**
        - `str`: The title of the recipe.
        """
        return self.title
