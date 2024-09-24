from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.

    This serializer handles the conversion of Comment model instances to and from JSON. It includes:

    * `author_email`: The email of the author, which is derived from the related `author` field and is read-only.
    * `content`: The content of the comment.
    * `created_at`: The timestamp when the comment was created (read-only).
    * `updated_at`: The timestamp when the comment was last updated (read-only).
    * `info`: Optional field related to the `info` this comment belongs to.
    * `recipe`: Optional field related to the `recipe` this comment belongs to.

    Fields:
        - `id`: The unique identifier of the comment.
        - `content`: The textual content of the comment.
        - `author_email`: The email address of the comment's author (read-only).
        - `created_at`: The timestamp when the comment was created (read-only).
        - `updated_at`: The timestamp when the comment was last updated (read-only).
        - `info`: The ID of the related `info` object.
        - `recipe`: The ID of the related `recipe` object.

    Read-Only Fields:
        - `author`: The user who created the comment (read-only).
        - `created_at`: The creation timestamp of the comment (read-only).
        - `updated_at`: The last update timestamp of the comment (read-only).
    """
    author_email = serializers.EmailField(source='author.email', read_only=True)
    author_name = serializers.CharField(source='author.author_name', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author_email', 'author_name', 'created_at', 'updated_at', 'info', 'recipe']
        read_only_fields = ['author', 'created_at', 'updated_at']
