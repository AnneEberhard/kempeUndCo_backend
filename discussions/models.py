import io
import os
from django.db import models
from django.conf import settings
from ancestors.models import Person
from utils.html_cleaner import clean_html
from PIL import Image, UnidentifiedImageError
from django.core.files.base import ContentFile
import uuid


def pdf_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    # Eindeutigen Dateinamen generieren, z.B. mit UUID
    filename = f"{uuid.uuid4().hex}.{ext}"
    # Optionaler Unterordner nach Beitrag-ID o.ä.
    return os.path.join('discussions', filename)



class Discussion(models.Model):
    """
    Model representing a discussion linked to a specific person.

    The Discussion model is linked to a Person through a one-to-one relationship.
    It stores metadata about when the discussion was created and last updated.

    Fields:
    - person: A one-to-one link to the Person model, representing the individual
      associated with this discussion.
    - created_at: The timestamp when the discussion was created. Automatically set.
    - updated_at: The timestamp when the discussion was last updated. Automatically updated.
    """
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name='discussion')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DiscussionEntry(models.Model):
    """
    Model representing an entry within a discussion.

    The DiscussionEntry model is linked to a Discussion through a foreign key relationship
    and represents an individual message or entry within that discussion. Each entry
    has an author and can contain a title and content, along with timestamps
    for when the entry was created and last updated.

    Fields:
    - discussion: A foreign key link to the Discussion model, representing the discussion
      to which this entry belongs.
    - author: A foreign key link to the User model, representing the author of this entry.
    - title: An optional title for the discussion entry.
    - content: The main text content of the discussion entry.
    - created_at: The timestamp when the entry was created. Automatically set.
    - updated_at: The timestamp when the entry was last updated. Automatically updated.
    """
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='entries')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Titel')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_1 = models.FileField(upload_to='discussions/', null=True, blank=True)
    image_1_thumbnail = models.ImageField(upload_to='discussions/thumbnails/', null=True, blank=True)
    image_2 = models.FileField(upload_to='discussions/', null=True, blank=True)
    image_2_thumbnail = models.ImageField(upload_to='discussions/thumbnails/', null=True, blank=True)
    image_3 = models.FileField(upload_to='discussions/', null=True, blank=True)
    image_3_thumbnail = models.ImageField(upload_to='discussions/thumbnails/', null=True, blank=True)
    image_4 = models.FileField(upload_to='discussions/', null=True, blank=True)
    image_4_thumbnail = models.ImageField(upload_to='discussions/thumbnails/', null=True, blank=True)

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
            old_entry = DiscussionEntry.objects.get(pk=self.pk)
            for i in range(1, 5):
                old_image = getattr(old_entry, f'image_{i}')
                new_image = getattr(self, f'image_{i}')
                if old_image and old_image != new_image:
                    if os.path.isfile(old_image.path):
                        os.remove(old_image.path)
                    thumbnail_field = f'image_{i}_thumbnail'
                    old_thumbnail = getattr(old_entry, thumbnail_field)
                    if old_thumbnail and os.path.isfile(old_thumbnail.path):
                        os.remove(old_thumbnail.path)

                    setattr(self, thumbnail_field, None)

        if self.image_1 and not self.image_1_thumbnail:
            self.create_thumbnail(self.image_1, 'image_1_thumbnail')
        if self.image_2 and not self.image_2_thumbnail:
            self.create_thumbnail(self.image_2, 'image_2_thumbnail')
        if self.image_3 and not self.image_3_thumbnail:
            self.create_thumbnail(self.image_3, 'image_3_thumbnail')
        if self.image_4 and not self.image_4_thumbnail:
            self.create_thumbnail(self.image_4, 'image_4_thumbnail')

        super().save(*args, **kwargs)

        self.discussion.updated_at = self.updated_at
        self.discussion.save(update_fields=['updated_at'])

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
        Returns a string representation of the DiscussionEntry instance.

        Returns:
            str: The title of the informational entry.
        """
        return self.title
