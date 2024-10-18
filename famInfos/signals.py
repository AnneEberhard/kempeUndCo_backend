import os
from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models import Q
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from accounts.models import CustomUser
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


@receiver(post_save, sender=FamInfo)
def send_faminfo_alert(sender, instance, created, **kwargs):
    """
    Send an alert to users whose families match the FamInfo's families.
    Only filled family fields of the instance are considered in the filtering.
    """
    if created:
        users_to_notify = CustomUser.objects.filter(alert_faminfo=True)

        family_filter = Q()

        if instance.family_1:
            family_filter |= Q(family_1=instance.family_1) | Q(family_2=instance.family_1)
        if instance.family_2:
            family_filter |= Q(family_1=instance.family_2) | Q(family_2=instance.family_2)

        users_to_notify = users_to_notify.filter(family_filter)

        print("Benachrichtigung an folgende Benutzer gesendet:", users_to_notify)

        for user in users_to_notify:

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            unsubscribe_url = f"{settings.BACKEND_URL}/unsubscribe/{uid}/{token}/faminfo/"
            
            send_mail(
                'Neue Familieninfo verfügbar',
                f'Hallo {user.username}, es gibt neue Informationen zu deiner Familie auf KempeUndCo: {instance.title}.'
                f'Wenn du keine Benachrichtigungen zu den Familien-Infos mehr erhalten möchtest, klicke hier: {unsubscribe_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
