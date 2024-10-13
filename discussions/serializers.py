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
        ref_name = 'DiscussionsPersonSerializer'


class DiscussionEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for the DiscussionEntry model.

    This serializer manages the representation of individual discussion entries.
    The 'author' field is read-only and is represented by the author's string
    representation. Other fields include 'id', 'title', 'content', 'created_at',
    and 'updated_at'.
    """
    author = serializers.StringRelatedField(read_only=True)
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
        model = DiscussionEntry
        fields = ['id', 'author', 'author_name', 'title', 'content', 'created_at', 'updated_at',
                  'image_1', 'image_2', 'image_3', 'image_4',
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
