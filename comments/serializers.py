from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(source='author.email', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author_email', 'created_at', 'updated_at', 'info', 'recipe']
        read_only_fields = ['author', 'created_at', 'updated_at']
