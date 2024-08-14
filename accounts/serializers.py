from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for obtaining JWT tokens using email and password.

    Validates user credentials and returns a pair of access and refresh tokens along with user details.

    Fields:
    - email: string
    - password: string

    Responses:
    - tokens: JWT access and refresh tokens
    - user: User details (id, email, username, is_active)
    """
    def validate(self, attrs):
        """
        Validate user credentials.

        Authenticate the user using email and password, and ensure the account is active.
        Return JWT tokens and user details if valid.

        Parameters:
        - attrs: Dictionary containing 'email' and 'password'

        Returns:
        - Dictionary containing JWT tokens and user details

        Raises:
        - serializers.ValidationError: If authentication fails or account is inactive
        """
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
    """
    Serializer for user registration.

    Handles the creation of a new user account with the necessary details.

    Fields:
    - email: string
    - password: string
    - first_name: string
    - last_name: string
    - guarantor: string (optional)
    - guarantor_email: string (optional)
    - family_1: string (optional)
    - family_2: string (optional)
    """
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name', 'guarantor', 'guarantor_email', 'family_1', 'family_2']

    def generate_random_username(self, email):
        """
        Generate a random username based on the email.

        Create a base username from the email prefix and append a random string.

        Parameters:
        - email: User's email address

        Returns:
        - string: Generated username
        """
        import random
        import string
        base_username = email.split('@')[0]
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        return base_username + random_string

    def create(self, validated_data):
        """
        Create a new user with the validated data.

        Check if a username is provided, otherwise generate one. Create the user with the provided details.

        Parameters:
        - validated_data: Dictionary containing validated user data

        Returns:
        - CustomUser: The created user instance
        """
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
            family_1=validated_data['family'],
            family_2='',
            username=validated_data['username']
        )
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for password reset request.

    Handles validation of the user's email for password reset.

    Fields:
    - email: string
    """
    email = serializers.EmailField()


class SetNewPasswordSerializer(serializers.Serializer):
    """
    Serializer for setting a new password.

    Handles validation and setting of the new password.

    Fields:
    - password: string (write-only, min length 8, max length 128)
    """
    password = serializers.CharField(write_only=True, min_length=8, max_length=128)
