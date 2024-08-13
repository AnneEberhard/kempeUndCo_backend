from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
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
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):

    FAMILY_CHOICES = [
        ('kempe', 'Stammbaum Kempe'),
        ('huenten', 'Stammbaum Hünten'),
        # Weitere Familienbäume hinzufügen, wenn nötig
    ]
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    guarantor = models.BooleanField(default=False)
    guarantor_email = models.EmailField(blank=True, null=True)
    family_1 = models.CharField(choices=FAMILY_CHOICES, max_length=50, blank=True, verbose_name='Stammbaum 1')
    family_2 = models.CharField(choices=FAMILY_CHOICES, max_length=50, blank=True, verbose_name='Stammbaum 2')
    notes = models.TextField(null=True, blank=True, verbose_name='Notizen')

    objects = CustomUserManager()

    def __str__(self):
        return self.email
