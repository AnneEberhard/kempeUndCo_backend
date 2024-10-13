import os
from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from famInfos.models import FamInfo
from kempeUndCo_backend.settings import EMAIL_HOST_USER


@receiver(post_delete, sender=FamInfo)
def delete_images_on_famInfo_delete(sender, instance, **kwargs):
    """
    Deletes associated image files and thumbnails when an famInfo instance is deleted.
    """
    for field in ['image_1', 'image_2', 'image_3', 'image_4']:
        image = getattr(instance, field)
        if image and os.path.isfile(image.path):
            os.remove(image.path)

        thumbnail_field = f'{field}'
        thumbnail = getattr(instance, thumbnail_field)
        if thumbnail and os.path.isfile(thumbnail.path):
            os.remove(thumbnail.path)


# @receiver(post_save, sender=FamInfo)
# def notify_new_famInfo(sender, instance, created, **kwargs):
#     if created:
#         send_mail(
#             'Neue famInfo erstellt',
#             f'Es wurde eine neue famInfo mit dem Titel "{instance.title}" auf der Webseite KempeUndCo erstellt.',
#             settings.DEFAULT_FROM_EMAIL,
#             [EMAIL_HOST_USER],
#             fail_silently=False,
#         )

