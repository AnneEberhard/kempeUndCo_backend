from rest_framework import serializers
from .models import Info


class InfoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Info model, including additional fields for image URLs.

    This serializer converts `Info` model instances into JSON format and provides additional fields
    to include the absolute URLs of associated images. It also includes the email of the author and
    handles the creation and updating of `Info` instances.

    Attributes:
        author_email (serializers.EmailField): The email of the author, sourced from the related user.
        image_1_url (serializers.SerializerMethodField): The absolute URL of the first image, if available.
        image_2_url (serializers.SerializerMethodField): The absolute URL of the second image, if available.
        image_3_url (serializers.SerializerMethodField): The absolute URL of the third image, if available.
        image_4_url (serializers.SerializerMethodField): The absolute URL of the fourth image, if available.

    Meta:
        model (Info): The model associated with this serializer.
        fields (list): The list of fields to be included in the serialized representation.
        read_only_fields (list): Fields that are read-only and not expected to be modified by clients.
    """
    author_email = serializers.EmailField(source='author.email', read_only=True)
    image_1_url = serializers.SerializerMethodField()
    image_2_url = serializers.SerializerMethodField()
    image_3_url = serializers.SerializerMethodField()
    image_4_url = serializers.SerializerMethodField()

    class Meta:
        model = Info
        fields = [
            'id', 'title', 'content', 'author_email', 'created_at', 'updated_at',
            'image_1', 'image_2', 'image_3', 'image_4',
            'image_1_url', 'image_2_url', 'image_3_url', 'image_4_url', 'family_1', 'family_2'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at']

    def get_image_1_url(self, obj):
        """
        Returns the absolute URL of the first image if it exists.

        Args:
            obj (Info): The instance of the Info model.

        Returns:
            str or None: The absolute URL of the first image or None if the image is not available.
        """
        return self.build_absolute_uri(obj.image_1.url) if obj.image_1 else None

    def get_image_2_url(self, obj):
        """
        Returns the absolute URL of the second image if it exists.

        Args:
            obj (Info): The instance of the Info model.

        Returns:
            str or None: The absolute URL of the second image or None if the image is not available.
        """
        return self.build_absolute_uri(obj.image_2.url) if obj.image_2 else None

    def get_image_3_url(self, obj):
        """
        Returns the absolute URL of the third image if it exists.

        Args:
            obj (Info): The instance of the Info model.

        Returns:
            str or None: The absolute URL of the third image or None if the image is not available.
        """
        return self.build_absolute_uri(obj.image_3.url) if obj.image_3 else None

    def get_image_4_url(self, obj):
        """
        Returns the absolute URL of the fourth image if it exists.

        Args:
            obj (Info): The instance of the Info model.

        Returns:
            str or None: The absolute URL of the fourth image or None if the image is not available.
        """
        return self.build_absolute_uri(obj.image_4.url) if obj.image_4 else None

    def build_absolute_uri(self, relative_url):
        """
        Constructs an absolute URI from a relative URL.

        Args:
            relative_url (str): The relative URL to be converted.

        Returns:
            str: The absolute URI constructed from the relative URL.
        """
        request = self.context.get('request')
        return request.build_absolute_uri(relative_url)
