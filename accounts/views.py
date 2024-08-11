from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser
from .serializers import RegisterSerializer
from django.core.mail import send_mail
from django.conf import settings

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        if user.guarantor:
            # Sende E-Mail an den Guarantor
            send_mail(
                'Guarantor Confirmation',
                'Please confirm your role as a guarantor for {}'.format(user.email),
                settings.DEFAULT_FROM_EMAIL,
                [user.guarantor_email],
            )
        else:
            # Sende E-Mail an den neuen Nutzer
            send_mail(
                'Welcome!',
                'Welcome to our platform, {}'.format(user.username),
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )