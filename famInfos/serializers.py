from rest_framework import serializers
from .models import FamInfo


class FamInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for the famInfo model, including additional fields for image URLs.

    This serializer converts `famInfo` model instances into JSON format and provides additional fields
    to include the absolute URLs of associated images. It also includes the email of the author and
    handles the creation and updating of `famInfo` instances.

    Attributes:
        author_email (serializers.EmailField): The email of the author, sourced from the related user.
        image_1_url (serializers.SerializerMethodField): The absolute URL of the first image, if available.
        image_2_url (serializers.SerializerMethodField): The absolute URL of the second image, if available.
        image_3_url (serializers.SerializerMethodField): The absolute URL of the third image, if available.
        image_4_url (serializers.SerializerMethodField): The absolute URL of the fourth image, if available.
        image_1_thumbnail_url`: The absolute URL for the first thumbnail (computed field).
        image_2_thumbnail_url`: The absolute URL for the second thumbnail (computed field).
        image_3_thumbnail_url`: The absolute URL for the third thumbnail (computed field).
        image_4_thumbnail_url`: The absolute URL for the fourth thumbnail (computed field).

    Meta:
        model (famInfo): The model associated with this serializer.
        fields (list): The list of fields to be included in the serialized representation.
        read_only_fields (list): Fields that are read-only and not expected to be modified by clients.
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
        model = FamInfo
        fields = [
            'id', 'title', 'content', 'author_email', 'author_name', 'created_at', 'updated_at',
            'image_1', 'image_2', 'image_3', 'image_4', 'family_1', 'family_2',
            'image_1_url', 'image_2_url', 'image_3_url', 'image_4_url',
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
