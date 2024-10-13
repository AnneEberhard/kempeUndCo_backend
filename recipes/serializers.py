from rest_framework import serializers
from .models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Recipe` model.

    This serializer handles the serialization and deserialization of `Recipe` instances,
    including handling of image URLs and author email.

    **Fields:**
    - `id`: The unique identifier of the recipe.
    - `title`: The title of the recipe.
    - `content`: The content or instructions of the recipe.
    - `author_email`: The email address of the recipe's author (read-only).
    - `created_at`: The timestamp when the recipe was created (read-only).
    - `updated_at`: The timestamp when the recipe was last updated (read-only).
    - `image_1_url`: The absolute URL for the first image (computed field).
    - `image_2_url`: The absolute URL for the second image (computed field).
    - `image_3_url`: The absolute URL for the third image (computed field).
    - `image_4_url`: The absolute URL for the fourth image (computed field).
    - `image_1_thumbnail_url`: The absolute URL for the first thumbnail (computed field).
    - `image_2_thumbnail_url`: The absolute URL for the second thumbnail (computed field).
    - `image_3_thumbnail_url`: The absolute URL for the third thumbnail (computed field).
    - `image_4_thumbnail_url`: The absolute URL for the fourth thumbnail (computed field).
    - `family_1`: The first family tree associated with the recipe.
    - `family_2`: The second family tree associated with the recipe.

    **Read-Only Fields:**
    - `author`: The author of the recipe (read-only).
    - `created_at`: The timestamp when the recipe was created (read-only).
    - `updated_at`: The timestamp when the recipe was last updated (read-only).
    """
    author_email = serializers.EmailField(source='author.email', read_only=True)
    author_name = serializers.CharField(source='author.author_name', read_only=True)
    image_1 = serializers.FileField(required=False)
    image_2 = serializers.FileField(required=False)
    image_3 = serializers.FileField(required=False)
    image_4 = serializers.FileField(required=False)
    image_1_url = serializers.SerializerMethodField()
    image_2_url = serializers.SerializerMethodField()
    image_3_url = serializers.SerializerMethodField()
    image_4_url = serializers.SerializerMethodField()
    image_1_thumbnail_url = serializers.SerializerMethodField()
    image_2_thumbnail_url = serializers.SerializerMethodField()
    image_3_thumbnail_url = serializers.SerializerMethodField()
    image_4_thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'content', 'author_email', 'author_name', 'created_at', 'updated_at',
            'image_1', 'image_2', 'image_3', 'image_4',
            'image_1_url', 'image_2_url', 'image_3_url', 'image_4_url', 'family_1', 'family_2',
            'image_1_thumbnail_url', 'image_2_thumbnail_url', 'image_3_thumbnail_url', 'image_4_thumbnail_url',
        ]
        read_only_fields = ['author', 'created_at', 'updated_at']

    def get_image_1_url(self, obj):
        return self.build_absolute_uri(obj.image_1.url) if obj.image_1 else None

    def get_image_2_url(self, obj):
        return self.build_absolute_uri(obj.image_2.url) if obj.image_2 else None

    def get_image_3_url(self, obj):
        return self.build_absolute_uri(obj.image_3.url) if obj.image_3 else None

    def get_image_4_url(self, obj):
        return self.build_absolute_uri(obj.image_4.url) if obj.image_4 else None

    def get_image_1_thumbnail_url(self, obj):
        return self.build_absolute_uri(obj.image_1_thumbnail.url) if obj.image_1_thumbnail else None

    def get_image_2_thumbnail_url(self, obj):
        return self.build_absolute_uri(obj.image_2_thumbnail.url) if obj.image_2_thumbnail else None

    def get_image_3_thumbnail_url(self, obj):
        return self.build_absolute_uri(obj.image_3_thumbnail.url) if obj.image_3_thumbnail else None

    def get_image_4_thumbnail_url(self, obj):
        return self.build_absolute_uri(obj.image_4_thumbnail.url) if obj.image_4_thumbnail else None

    def build_absolute_uri(self, relative_url):
        request = self.context.get('request')
        return request.build_absolute_uri(relative_url)
