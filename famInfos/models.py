import os
from django.db import models
from django.conf import settings
from kempeUndCo_backend.constants import FAMILY_CHOICES
from utils.html_cleaner import clean_html
from PIL import Image, UnidentifiedImageError
import io
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os
import uuid


def pdf_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    # Eindeutigen Dateinamen generieren, z.B. mit UUID
    filename = f"{uuid.uuid4().hex}.{ext}"
    # Optionaler Unterordner nach Beitrag-ID o.ä.
    return os.path.join('famInfos', filename)


class FamInfo(models.Model):
    """
    Model representing an famInformational entry with optional images and associated family trees.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Image fields with custom upload paths
    image_1 = models.FileField(upload_to='famInfos/', null=True, blank=True)
    image_1_thumbnail = models.ImageField(upload_to='famInfos/thumbnails/', null=True, blank=True)
    image_2 = models.FileField(upload_to='famInfos/', null=True, blank=True)
    image_2_thumbnail = models.ImageField(upload_to='famInfos/thumbnails/', null=True, blank=True)
    image_3 = models.FileField(upload_to='famInfos/', null=True, blank=True)
    image_3_thumbnail = models.ImageField(upload_to='famInfos/thumbnails/', null=True, blank=True)
    image_4 = models.FileField(upload_to='famInfos/', null=True, blank=True)
    image_4_thumbnail = models.ImageField(upload_to='famInfos/thumbnails/', null=True, blank=True)

    family_1 = models.CharField(choices=FAMILY_CHOICES, max_length=100, blank=False, verbose_name='Stammbaum 1')
    family_2 = models.CharField(choices=FAMILY_CHOICES, max_length=50, blank=True, null=True, verbose_name='Stammbaum 2')

    pdf_1 = models.FileField(upload_to=pdf_upload_to, null=True, blank=True)
    pdf_1_name = models.CharField(max_length=255, null=True, blank=True) 
    pdf_2 = models.FileField(upload_to=pdf_upload_to, null=True, blank=True)
    pdf_2_name = models.CharField(max_length=255, null=True, blank=True) 
    pdf_3 = models.FileField(upload_to=pdf_upload_to, null=True, blank=True)
    pdf_3_name = models.CharField(max_length=255, null=True, blank=True) 
    pdf_4 = models.FileField(upload_to=pdf_upload_to, null=True, blank=True)
    pdf_4_name = models.CharField(max_length=255, null=True, blank=True) 

    def save(self, *args, **kwargs):
        """
        Overrides the save method to clean HTML from content and handle image file management.

        If the instance already exists (i.e., it's being updated), this method:
        - Cleans the HTML content of the entry.
        - Deletes old images that are being replaced by new ones.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.content = clean_html(self.content)

        if self.pk:
            old_famInfo = FamInfo.objects.get(pk=self.pk)
            for i in range(1, 5):
                old_image = getattr(old_famInfo, f'image_{i}')
                new_image = getattr(self, f'image_{i}')
                if old_image and old_image != new_image:
                    if os.path.isfile(old_image.path):
                        os.remove(old_image.path)
                    thumbnail_field = f'image_{i}_thumbnail'
                    old_thumbnail = getattr(old_famInfo, thumbnail_field)
                    if old_thumbnail and os.path.isfile(old_thumbnail.path):
                        os.remove(old_thumbnail.path)    
                    setattr(self, thumbnail_field, None)

        for i in range(1, 5):
            image_field = getattr(self, f'image_{i}')
            thumbnail_field_name = f'image_{i}_thumbnail'
# 
            if image_field and not getattr(self, thumbnail_field_name):
                self.create_thumbnail(image_field, thumbnail_field_name, i)

        super().save(*args, **kwargs)

    def create_thumbnail(self, image_field, thumbnail_field_name, index):
        """Erstellt ein Thumbnail für das gegebene Bildfeld."""
        try:
            with Image.open(image_field) as img:
                img = img.convert('RGB')
                img.thumbnail((200, 200))
                thumb_io = io.BytesIO()
                img.save(thumb_io, format='JPEG', quality=70)
    
                original_path = image_field.name
                base_name = os.path.basename(original_path)
                base_name, ext = os.path.splitext(base_name)
                thumb_name = f"{base_name}_thumbnail.jpg"
                thumb_file = ContentFile(thumb_io.getvalue(), name=thumb_name)
                setattr(self, thumbnail_field_name, thumb_file)
    
        except UnidentifiedImageError:
            # Datei ist kein Bild (z. B. PDF) → kein Thumbnail
            setattr(self, thumbnail_field_name, None)

    def __str__(self):
        """
        Returns a string representation of the famInfo instance.

        Returns:
            str: The title of the famInformational entry.
        """
        return self.title
