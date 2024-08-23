from rest_framework import serializers
from .models import Info

class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 'image_1', 'image_2', 'image_3', 'image_4']
        read_only_fields = ['author', 'created_at', 'updated_at']
