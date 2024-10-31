import os
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from accounts.models import CustomUser
from kempeUndCo_backend.settings import EMAIL_HOST_USER

from .models import DiscussionEntry


@receiver(post_delete, sender=DiscussionEntry)
def delete_images_on_entry_delete(sender, instance, **kwargs):
    """
    Deletes associated image files and thumbnails when a discussion entry instance is deleted.
    """
    for field in ['image_1', 'image_2', 'image_3', 'image_4']:
        image = getattr(instance, field)
        if image and os.path.isfile(image.path):
            os.remove(image.path)

        thumbnail_field = f'{field}_thumbnail'
        thumbnail = getattr(instance, thumbnail_field)
        if thumbnail and os.path.isfile(thumbnail.path):
            os.remove(thumbnail.path)


@receiver(post_delete, sender=DiscussionEntry)
def delete_empty_discussion(sender, instance, **kwargs):
    """
    Signal handler to delete the associated discussion if it has no more entries.
    Triggered after a DiscussionEntry is deleted.
    """
    discussion = instance.discussion
    if not discussion.entries.exists():  # Check if there are no more entries
        discussion.delete()  # Delete the discussion if it's empty


# @receiver(post_save, sender=DiscussionEntry)
# def notify_new_discussion(sender, instance, created, **kwargs):
#     if created:
#         
#         print(instance.discussion.person.name)
#         send_mail(
#             'Neuer Diskussionsbeitrag erstellt',
#             f'Es wurde ein neuer Diskussionsbeitrag zu Person "{instance.discussion.person.name}" auf der Webseite KempeUndCo erstellt.',
#             settings.DEFAULT_FROM_EMAIL,
#             [EMAIL_HOST_USER],
#             fail_silently=False,
#         )


@receiver(post_save, sender=DiscussionEntry)
def notify_new_discussionEntry(sender, instance, created, **kwargs):
    if created:
        related_person = instance.discussion.person
        users_to_notify = CustomUser.objects.filter(alert_discussion=True)

        family_filter = Q()
        if related_person.family_1:
            family_filter |= Q(family_1=related_person.family_1) | Q(family_2=related_person.family_1)
        if related_person.family_2:
            family_filter |= Q(family_1=related_person.family_2) | Q(family_2=related_person.family_2)

        users_to_notify = users_to_notify.filter(family_filter)
        for user in users_to_notify:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            unsubscribe_url = f"{settings.BACKEND_URL}/unsubscribe/{uid}/{token}/discussion/"

            html_content = render_to_string('emails/new_discussion_alert.html', {
                'person_name': instance.discussion.person.name,
                'unsubscribe_url': unsubscribe_url,
                'user.first_name': user.first_name
            })
            text_content = strip_tags(html_content)
            print('email')
            email = EmailMultiAlternatives(
                subject='Neuer Diskussionsbeitrag zur Stammfolge',
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

           #send_mail(
           #    'Neuer Diskussionsbeitrag erstellt',
           #    f'Hallo {user.username}! Es wurde ein neuer Diskussionsbeitrag zu Person "{instance.discussion.person.name}" auf der Webseite KempeUndCo erstellt. '
           #    f'Wenn du keine Benachrichtigungen zur Webseitendiskussion mehr erhalten möchtest, klicke hier: {unsubscribe_url}',
           #    settings.DEFAULT_FROM_EMAIL,
           #    [user.email],
           #    fail_silently=False,
           #)