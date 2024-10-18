import os
from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

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


# @receiver(post_save, sender=Info)
# def notify_new_info(sender, instance, created, **kwargs):
#     if created:
#         print('notify single')
#         send_mail(
#             'Neue Info erstellt',
#             f'Es wurde eine neue Info mit dem Titel "{instance.title}" auf der Webseite KempeUndCo erstellt.',
#             settings.DEFAULT_FROM_EMAIL,
#             [EMAIL_HOST_USER],
#             fail_silently=False,
#         )


@receiver(post_save, sender=Info)
def notify_new_Info(sender, instance, created, **kwargs):
    print('notify list')
    if created:
        users_to_notify = CustomUser.objects.filter(alert_info=True)

        for user in users_to_notify:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            unsubscribe_url = f"{settings.BACKEND_URL}/unsubscribe/{uid}/{token}/info/"
            send_mail(
                'Neue Info erstellt',
                f'Hallo {user.username}! Es wurde eine neue Webseiten-Info mit dem Titel "{instance.title}" auf KempeUndCo erstellt. '
                f'Wenn du keine Benachrichtigungen zur Webseitendiskussion mehr erhalten möchtest, klicke hier: {unsubscribe_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
