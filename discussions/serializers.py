# discussions/serializers.py
from rest_framework import serializers
from .models import Discussion, DiscussionEntry

class DiscussionEntrySerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = DiscussionEntry
        fields = ['id', 'author', 'content', 'created_at', 'updated_at']

class DiscussionSerializer(serializers.ModelSerializer):
    entries = DiscussionEntrySerializer(many=True, read_only=True)

    class Meta:
        model = Discussion
        fields = ['id', 'person', 'created_at', 'updated_at', 'entries']
