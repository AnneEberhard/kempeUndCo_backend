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
    - `image_1`: The first image associated with the recipe.
    - `image_2`: The second image associated with the recipe.
    - `image_3`: The third image associated with the recipe.
    - `image_4`: The fourth image associated with the recipe.
    - `image_1_url`: The absolute URL for the first image (computed field).
    - `image_2_url`: The absolute URL for the second image (computed field).
    - `image_3_url`: The absolute URL for the third image (computed field).
    - `image_4_url`: The absolute URL for the fourth image (computed field).
    - `family_1`: The first family tree associated with the recipe.
    - `family_2`: The second family tree associated with the recipe.

    **Read-Only Fields:**
    - `author`: The author of the recipe (read-only).
    - `created_at`: The timestamp when the recipe was created (read-only).
    - `updated_at`: The timestamp when the recipe was last updated (read-only).
    """
    author_email = serializers.EmailField(source='author.email', read_only=True)
    image_1_url = serializers.SerializerMethodField()
    image_2_url = serializers.SerializerMethodField()
    image_3_url = serializers.SerializerMethodField()
    image_4_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'content', 'author_email', 'created_at', 'updated_at',
            'image_1', 'image_2', 'image_3', 'image_4',
            'image_1_url', 'image_2_url', 'image_3_url', 'image_4_url', 'family_1', 'family_2'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at']

    def get_image_1_url(self, obj):
        """
        Returns the absolute URL for `image_1`.

        If `image_1` is not present, returns `None`.

        **Parameters:**
        - `obj`: The `Recipe` instance being serialized.

        **Returns:**
        - `str` or `None`: The absolute URL of `image_1` if available, otherwise `None`.
        """
        return self.build_absolute_uri(obj.image_1.url) if obj.image_1 else None

    def get_image_2_url(self, obj):
        """
        Returns the absolute URL for `image_2`.

        If `image_2` is not present, returns `None`.

        **Parameters:**
        - `obj`: The `Recipe` instance being serialized.

        **Returns:**
        - `str` or `None`: The absolute URL of `image_2` if available, otherwise `None`.
        """
        return self.build_absolute_uri(obj.image_2.url) if obj.image_2 else None

    def get_image_3_url(self, obj):
        """
        Returns the absolute URL for `image_3`.

        If `image_3` is not present, returns `None`.

        **Parameters:**
        - `obj`: The `Recipe` instance being serialized.

        **Returns:**
        - `str` or `None`: The absolute URL of `image_3` if available, otherwise `None`.
        """
        return self.build_absolute_uri(obj.image_3.url) if obj.image_3 else None

    def get_image_4_url(self, obj):
        """
        Returns the absolute URL for `image_4`.

        If `image_4` is not present, returns `None`.

        **Parameters:**
        - `obj`: The `Recipe` instance being serialized.

        **Returns:**
        - `str` or `None`: The absolute URL of `image_4` if available, otherwise `None`.
        """
        return self.build_absolute_uri(obj.image_4.url) if obj.image_4 else None

    def build_absolute_uri(self, relative_url):
        """
        Builds the absolute URI from a relative URL.

        **Parameters:**
        - `relative_url`: The relative URL to be converted to an absolute URI.

        **Returns:**
        - `str`: The absolute URI built from the relative URL.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(relative_url)
