import os
from django.db import models
from django.conf import settings
from utils.html_cleaner import clean_html

class Recipe(models.Model):
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

    def save(self, *args, **kwargs):
        self.content = clean_html(self.content)

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
        return self.title
