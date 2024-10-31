import os
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from accounts.models import CustomUser
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


# @receiver(post_save, sender=Recipe)
# def notify_new_recipe(sender, instance, created, **kwargs):
#     if created:
#         send_mail(
#             'Neues Rezept erstellt',
#             f'Es wurde ein neues Rezept mit dem Titel "{instance.title}" auf der Webseite KempeUndCo erstellt.',
#             settings.DEFAULT_FROM_EMAIL,
#             [EMAIL_HOST_USER],
#             fail_silently=False,
#         )

@receiver(post_save, sender=Recipe)
def notify_new_recipe(sender, instance, created, **kwargs):
    if created:
        users_to_notify = CustomUser.objects.filter(alert_recipe=True)

        for user in users_to_notify:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            unsubscribe_url = f"{settings.BACKEND_URL}/unsubscribe/{uid}/{token}/recipe/"
            html_content = render_to_string('emails/new_recipe_alert.html', {
                'title': instance.title,
                'unsubscribe_url': unsubscribe_url,
                'user.first_name': user.first_name
            })
            text_content = strip_tags(html_content)
            print('email')
            email = EmailMultiAlternatives(
                subject='Neues Rezept erstellt',
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            email.attach_alternative(html_content, "text/html")
            email.send()


          # send_mail(
          #     'Neues Rezept erstellt',
          #     f'Es wurde ein neues Rezept mit dem Titel "{instance.title}" auf der Webseite KempeUndCo erstellt. '
          #     f'Wenn du keine Benachrichtigungen zu den Rezepten mehr erhalten möchtest, klicke hier: {unsubscribe_url}',
          #     settings.DEFAULT_FROM_EMAIL,
          #     [user.email],
          #     fail_silently=False,
          # )
