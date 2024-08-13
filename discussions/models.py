from django.db import models
from django.conf import settings
from ancestors.models import Person


class Discussion(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name='discussion')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DiscussionEntry(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='entries')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
