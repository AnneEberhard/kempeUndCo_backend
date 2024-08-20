# discussions/serializers.py
from rest_framework import serializers

from ancestors.models import Person
from .models import Discussion, DiscussionEntry


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name']


class DiscussionEntrySerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = DiscussionEntry
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at']


class DiscussionSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    entries = DiscussionEntrySerializer(many=True, read_only=True)

    class Meta:
        model = Discussion
        fields = ['id', 'person', 'created_at', 'updated_at', 'entries']
