import os
from django.db import models
from django.conf import settings
from kempeUndCo_backend.constants import FAMILY_CHOICES
from utils.html_cleaner import clean_html
from PIL import Image, UnidentifiedImageError
import io
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import uuid


def pdf_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    # Eindeutigen Dateinamen generieren, z.B. mit UUID
    filename = f"{uuid.uuid4().hex}.{ext}"
    # Optionaler Unterordner nach Beitrag-ID o.ä.
    return os.path.join('infos', filename)


class Info(models.Model):
    """
    Model representing an informational entry with optional images and associated family trees.

    Attributes:
        title (CharField): The title of the informational entry, with a maximum length of 255 characters.
        content (TextField): The content of the entry, which is cleaned of HTML tags before saving.
        author (ForeignKey): The user who created the entry, linked to the AUTH_USER_MODEL.
        created_at (DateTimeField): Timestamp when the entry was created, automatically set on creation.
        updated_at (DateTimeField): Timestamp when the entry was last updated, automatically updated on save.
        image_1 (FileField): The first image associated with the entry, stored under the 'infos/' directory.
        image_2 (FileField): The second image associated with the entry, stored under the 'infos/' directory.
        image_3 (FileField): The third image associated with the entry, stored under the 'infos/' directory.
        image_4 (FileField): The fourth image associated with the entry, stored under the 'infos/' directory.
        family_1 (CharField): The first family tree associated with the entry, chosen from FAMILY_CHOICES.
        family_2 (CharField): The second family tree associated with the entry, chosen from FAMILY_CHOICES.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Image fields with custom upload paths
    image_1 = models.FileField(upload_to='infos/', null=True, blank=True)
    image_1_thumbnail = models.ImageField(upload_to='infos/thumbnails/', null=True, blank=True)
    image_2 = models.FileField(upload_to='infos/', null=True, blank=True)
    image_2_thumbnail = models.ImageField(upload_to='infos/thumbnails/', null=True, blank=True)
    image_3 = models.FileField(upload_to='infos/', null=True, blank=True)
    image_3_thumbnail = models.ImageField(upload_to='infos/thumbnails/', null=True, blank=True)
    image_4 = models.FileField(upload_to='infos/', null=True, blank=True)
    image_4_thumbnail = models.ImageField(upload_to='infos/thumbnails/', null=True, blank=True)

    pdf_1 = models.FileField(upload_to=pdf_upload_to, null=True, blank=True)
    pdf_1_name = models.CharField(max_length=255, null=True, blank=True) 
    pdf_2 = models.FileField(upload_to=pdf_upload_to, null=True, blank=True)
    pdf_2_name = models.CharField(max_length=255, null=True, blank=True) 
    pdf_3 = models.FileField(upload_to=pdf_upload_to, null=True, blank=True)
    pdf_3_name = models.CharField(max_length=255, null=True, blank=True) 
    pdf_4 = models.FileField(upload_to=pdf_upload_to, null=True, blank=True)
    pdf_4_name = models.CharField(max_length=255, null=True, blank=True) 

    family_1 = models.CharField(choices=FAMILY_CHOICES, max_length=100, blank=False, verbose_name='Stammbaum 1')
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
        Overrides the save method to clean HTML from content and handle image file management.

        If the instance already exists (i.e., it's being updated), this method:
        - Cleans the HTML content of the entry.
        - Deletes old images that are being replaced by new ones.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.content = clean_html(self.content)

        # for i in range(1, 5):
        #     image_field = getattr(self, f'image_{i}')
        #     if image_field and hasattr(image_field, 'file'):
        #        compressed_image = self.compress_image(image_field.file)
        #         setattr(self, f'image_{i}', compressed_image)

        if self.pk:
            old_info = Info.objects.get(pk=self.pk)
            for i in range(1, 5):
                old_image = getattr(old_info, f'image_{i}')
                new_image = getattr(self, f'image_{i}')
                if old_image and old_image != new_image:
                    if os.path.isfile(old_image.path):
                        os.remove(old_image.path)

        if self.image_1 and not self.image_1_thumbnail:
            self.create_thumbnail(self.image_1, 'image_1_thumbnail')
        if self.image_2 and not self.image_2_thumbnail:
            self.create_thumbnail(self.image_2, 'image_2_thumbnail')
        if self.image_3 and not self.image_3_thumbnail:
            self.create_thumbnail(self.image_3, 'image_3_thumbnail')
        if self.image_4 and not self.image_4_thumbnail:
            self.create_thumbnail(self.image_4, 'image_4_thumbnail')

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
        Returns a string representation of the Info instance.

        Returns:
            str: The title of the informational entry.
        """
        return self.title
