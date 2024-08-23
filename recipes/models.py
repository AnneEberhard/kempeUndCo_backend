from django.db import models
from django.conf import settings
from utils.html_cleaner import clean_html

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    instructions = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Image fields with custom upload paths
    image_1 = models.FileField(upload_to='recipes/', null=True, blank=True)
    image_2 = models.FileField(upload_to='recipes/', null=True, blank=True)
    image_3 = models.FileField(upload_to='recipes/', null=True, blank=True)
    image_4 = models.FileField(upload_to='recipes/', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.instructions = clean_html(self.instructions)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
