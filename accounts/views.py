from django.shortcuts import redirect
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from .models import CustomUser
from .serializers import PasswordResetRequestSerializer, RegisterSerializer,CustomTokenObtainPairSerializer, SetNewPasswordSerializer


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegistrationView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user_data = serializer.validated_data

        if user_data.get('guarantor'):
            guarantor_email = user_data.get('guarantor_email')
            try:
                guarantor_user = CustomUser.objects.get(email=guarantor_email)

                # Benutzer erstellen
                user = serializer.save()

                # Senden einer Aktivierungs-E-Mail an den Bürgen
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                activation_link = f"{settings.BACKEND_URL}/activate/{uidb64}/{token}/"

                subject = 'Bürgen für neuen Nutzer der Familienwebseite'
                html_message = render_to_string('guarantor_email.html', {'activation_link': activation_link, 'user': user})
                plain_message = strip_tags(html_message)
                from_email = settings.NO_REPLY_EMAIL
                to_email = [guarantor_user.email]

                email = EmailMultiAlternatives(subject, plain_message, from_email, to=to_email, reply_to=[settings.REPLY_TO_EMAIL])
                email.attach_alternative(html_message, "text/html")
                email.send()

            except CustomUser.DoesNotExist:
                # Senden einer Benachrichtigungs-E-Mail an den neuen Benutzer, dass der Bürge nicht existiert
                subject = 'Ihr Bürge existiert nicht'
                html_message = render_to_string('guarantor_not_exist_email.html', {'user': user_data})
                plain_message = strip_tags(html_message)
                from_email = settings.NO_REPLY_EMAIL
                to_email = [user_data['email']]

                email = EmailMultiAlternatives(subject, plain_message, from_email, to=to_email, reply_to=[settings.REPLY_TO_EMAIL])
                email.attach_alternative(html_message, "text/html")
                email.send()

                raise serializers.ValidationError("Der angegebene Bürge existiert nicht.")
        else:
            # Benutzer erstellen
            user = serializer.save()

            # Senden einer Text-E-Mail mit weiteren Anweisungen
            subject = 'Herzlich Willkommen'
            html_message = render_to_string('no_guarantor_email.html')
            plain_message = strip_tags(html_message)
            from_email = settings.NO_REPLY_EMAIL
            to_email = [user.email]

            email = EmailMultiAlternatives(subject, plain_message, from_email, to=to_email, reply_to=[settings.REPLY_TO_EMAIL])
            email.attach_alternative(html_message, "text/html")
            email.send()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'success': 'Please check the respective email.'}, status=status.HTTP_201_CREATED)
    

class ActivationView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            # Senden einer Aktivierungsbestätigungs-E-Mail an den Benutzer
            subject = 'Konto wurde aktiviert'
            html_message = render_to_string('activation_email.html', {'user': user})
            plain_message = strip_tags(html_message)
            from_email = settings.NO_REPLY_EMAIL
            to_email = [user.email]

            email = EmailMultiAlternatives(subject, plain_message, from_email, to=to_email, reply_to=[settings.REPLY_TO_EMAIL])
            email.attach_alternative(html_message, "text/html")
            email.send()

            # Falls der Benutzer einen Bürgen hat, senden wir eine E-Mail an den Bürgen
            if user.guarantor:
                guarantor_email = user.guarantor_email
                try:
                    guarantor_user = CustomUser.objects.get(email=guarantor_email)

                    subject = 'Ein neuer Benutzer wurde aktiviert'
                    html_message = render_to_string('guarantor_activation_email.html', {'user': user})
                    plain_message = strip_tags(html_message)
                    from_email = settings.NO_REPLY_EMAIL
                    to_email = [guarantor_user.email]

                    email = EmailMultiAlternatives(subject, plain_message, from_email, to=to_email, reply_to=[settings.REPLY_TO_EMAIL])
                    email.attach_alternative(html_message, "text/html")
                    email.send()
                except CustomUser.DoesNotExist:
                    pass

            # Redirect to the frontend activation success page
            return redirect(f"{settings.FRONTEND_URL}/activation-success")
        else:
            # Redirect to the frontend activation failure page
            return redirect(f"{settings.FRONTEND_URL}/activation-failure")


class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = CustomUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f"{settings.FRONTEND_URL}/reset-password/{uidb64}/{token}/"

            subject = 'Passwort zurücksetzen'
            html_message = render_to_string('password_reset_email.html', {'reset_link': reset_link, 'user': user})
            plain_message = strip_tags(html_message)
            from_email = settings.NO_REPLY_EMAIL
            to_email = [user.email]

            email = EmailMultiAlternatives(subject, plain_message, from_email, to=to_email, reply_to=[settings.REPLY_TO_EMAIL])
            email.attach_alternative(html_message, "text/html")
            email.send()

            return Response({'success': 'Ein Link zum Zurücksetzen des Passworts wurde an Ihre E-Mail-Adresse gesendet.'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Ein Benutzer mit dieser E-Mail-Adresse existiert nicht.'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        serializer = SetNewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
            if not default_token_generator.check_token(user, token):
                return Response({'error': 'Token ist ungültig oder abgelaufen.'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'success': 'Das Passwort wurde erfolgreich zurückgesetzt.'}, status=status.HTTP_200_OK)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response({'error': 'Ungültiger Link.'}, status=status.HTTP_400_BAD_REQUEST)

