from rest_framework import serializers
from .models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
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
            'image_1_url', 'image_2_url', 'image_3_url', 'image_4_url'
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

    def build_absolute_uri(self, relative_url):
        request = self.context.get('request')
        return request.build_absolute_uri(relative_url)
