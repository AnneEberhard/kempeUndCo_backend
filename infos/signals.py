import os
from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from accounts.models import CustomUser
from infos.models import Info
from kempeUndCo_backend.settings import EMAIL_HOST_USER


@receiver(post_delete, sender=Info)
def delete_images_on_info_delete(sender, instance, **kwargs):
    """
    Deletes associated image files and thumbnails when an Info instance is deleted.
    """
    for field in ['image_1', 'image_2', 'image_3', 'image_4']:
        image = getattr(instance, field)
        if image and os.path.isfile(image.path):
            os.remove(image.path)

        thumbnail_field = f'{field}_thumbnail'
        thumbnail = getattr(instance, thumbnail_field)
        if thumbnail and os.path.isfile(thumbnail.path):
            os.remove(thumbnail.path)


@receiver(post_save, sender=Info)
def notify_new_info(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Neue Info erstellt',
            f'Es wurde eine neue Info mit dem Titel "{instance.title}" auf der Webseite KempeUndCo erstellt.',
            settings.DEFAULT_FROM_EMAIL,
            [EMAIL_HOST_USER],
            fail_silently=False,
        )

def notify_new_famInfo(sender, instance, created, **kwargs):
    if created:
        users_to_notify = CustomUser.objects.filter(alert_info=True)

        email_list = [user.email for user in users_to_notify]

        if email_list:
            send_mail(
                'Neue Info erstellt',
                f'Es wurde eine neue Info mit dem Titel "{instance.title}" auf der Webseite KempeUndCo erstellt.',
                settings.DEFAULT_FROM_EMAIL,
                email_list,
                fail_silently=False,
            )
        send_mail(
             'Neue Info erstellt',
             f'Es wurde eine neue Info mit dem Titel "{instance.title}" auf der Webseite KempeUndCo erstellt.',
             settings.DEFAULT_FROM_EMAIL,
             [EMAIL_HOST_USER],
             fail_silently=False,
        )
