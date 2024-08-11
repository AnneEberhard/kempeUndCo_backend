from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        authenticate_kwargs = {
            'email': attrs['email'],
            'password': attrs['password'],
        }
        user = authenticate(**authenticate_kwargs)

        if user is None or not user.is_active:
            raise serializers.ValidationError('Invalid credentials or inactive account')

        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'username': self.user.username,
            'is_active': self.user.is_active,
        }
        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name', 'guarantor', 'guarantor_email', 'family']

    def generate_random_username(self, email):
        import random
        import string
        base_username = email.split('@')[0]
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        return base_username + random_string

    def create(self, validated_data):
        # Check if username is provided, if not, generate one
        if not validated_data.get('username'):
            username = self.generate_random_username(validated_data['email'])
            validated_data['username'] = username

        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            guarantor=validated_data['guarantor'],
            guarantor_email=validated_data.get('guarantor_email'),
            family=validated_data['family'],
            username=validated_data['username']
        )
        return user