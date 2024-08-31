from rest_framework import serializers
from .models import Person, DiscussionEntry, Discussion

class PersonSerializer(serializers.ModelSerializer):
    """
    Serializer for the Person model.

    This serializer handles the conversion of Person objects to and from 
    their JSON representation. It includes the 'id' and 'name' fields of the Person.
    """
    class Meta:
        model = Person
        fields = ['id', 'name']


class DiscussionEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for the DiscussionEntry model.

    This serializer manages the representation of individual discussion entries. 
    The 'author' field is read-only and is represented by the author's string 
    representation. Other fields include 'id', 'title', 'content', 'created_at', 
    and 'updated_at'.
    """
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = DiscussionEntry
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at']


class DiscussionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Discussion model.

    This serializer encapsulates the details of a discussion related to a person, 
    including the person involved and the discussion entries. It uses the 
    `PersonSerializer` for the 'person' field and the `DiscussionEntrySerializer` 
    for the 'entries' field. The 'entries' field is read-only and supports 
    multiple entries. Fields include 'id', 'person', 'created_at', 'updated_at', 
    and 'entries'.
    """
    person = PersonSerializer()
    entries = DiscussionEntrySerializer(many=True, read_only=True)

    class Meta:
        model = Discussion
        fields = ['id', 'person', 'created_at', 'updated_at', 'entries']
