import os
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from kempeUndCo_backend.settings import EMAIL_HOST_USER

from .models import Comment

@receiver(post_save, sender=Comment)
def notify_new_comment(sender, instance, created, **kwargs):
    if created:
        title = ''
        if instance.info:
            title = instance.info.title
        elif instance.recipe:
            title = instance.recipe.title
        if title:
            send_mail(
                'Neuer Kommentar veröffentlicht',
                f'Es wurde ein neuer Kommentar zu "{title}" auf der Webseite KempeUndCo veröffentlicht.',
                settings.DEFAULT_FROM_EMAIL,
                [EMAIL_HOST_USER],
                fail_silently=False,
            )
        else:
            print('Kein Titel verfügbar für den Kommentar.')
