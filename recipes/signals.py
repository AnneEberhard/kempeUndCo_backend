import os
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from kempeUndCo_backend.settings import EMAIL_HOST_USER
from recipes.models import Recipe


@receiver(post_delete, sender=Recipe)
def delete_images_on_recipe_delete(sender, instance, **kwargs):
    """
    Deletes associated image files and thumbnails when a Recipe instance is deleted.
    """
    for field in ['image_1', 'image_2', 'image_3', 'image_4']:
        image = getattr(instance, field)
        if image and os.path.isfile(image.path):
            os.remove(image.path)

        thumbnail_field = f'{field}_thumbnail'
        thumbnail = getattr(instance, thumbnail_field)
        if thumbnail and os.path.isfile(thumbnail.path):
            os.remove(thumbnail.path)


@receiver(post_save, sender=Recipe)
def notify_new_recipe(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Neues Rezept erstellt',
            f'Es wurde ein neues Rezept mit dem Titel "{instance.title}" auf der Webseite KempeUndCo erstellt.',
            settings.DEFAULT_FROM_EMAIL,
            [EMAIL_HOST_USER],
            fail_silently=False,
        )
