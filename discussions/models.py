from django.db import models
from django.conf import settings
from ancestors.models import Person


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
