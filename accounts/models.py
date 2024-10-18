from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager

from kempeUndCo_backend.constants import FAMILY_CHOICES


class CustomUserManager(BaseUserManager):
    """
    Custom manager for CustomUser.

    Provides methods to create regular users and superusers with email as the unique identifier.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with the given email and password.

        Parameters:
        - email: User's email address
        - password: User's password
        - extra_fields: Additional fields for the user

        Returns:
        - CustomUser: The created user instance

        Raises:
        - ValueError: If the email is not provided
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)

        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with the given email and password.

        Parameters:
        - email: User's email address
        - password: User's password
        - extra_fields: Additional fields for the user

        Returns:
        - CustomUser: The created superuser instance
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    Uses email as the unique identifier instead of username and includes additional fields for family trees and guarantor information.

    Fields:
    - email: string, unique
    - guarantor: boolean, default False
    - guarantor_email: string, optional
    - family_1: string, optional, choices for first family tree
    - family_2: string, optional, choices for second family tree
    - notes: text, optional
    """

    email = models.EmailField(unique=True)
    author_name = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    guarantor = models.BooleanField(default=False)
    guarantor_email = models.EmailField(blank=True, null=True)
    family_1 = models.CharField(choices=FAMILY_CHOICES, max_length=50, blank=True, verbose_name='Stammbaum 1')
    family_2 = models.CharField(choices=FAMILY_CHOICES, max_length=50, blank=True, null=True, verbose_name='Stammbaum 2')
    notes = models.TextField(null=True, blank=True, verbose_name='Notizen')

    alert_faminfo = models.BooleanField(default=False, verbose_name='Familen-Info-Benachrichtigungen')
    alert_info = models.BooleanField(default=False, verbose_name='Website-Info-Benachrichtigungen')
    alert_recipe = models.BooleanField(default=False, verbose_name='Rezept-Benachrichtigungen')
    alert_discussion = models.BooleanField(default=False, verbose_name='Stammfolge-Diskussion-Benachrichtigungen')

    objects = CustomUserManager()

    @property
    def allowed_families(self):
        return [self.family_1, self.family_2] if self.family_2 else [self.family_1]

    def __str__(self):
        """
        Return the email address of the user.

        Returns:
        - string: User's email address
        """
        return self.email
