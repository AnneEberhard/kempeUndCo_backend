from django.shortcuts import render, redirect
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
from .serializers import ChangeAlertPreferencesSerializer, ChangeAuthorNameSerializer, ChangePasswordSerializer, PasswordResetRequestSerializer, RegisterSerializer, CustomTokenObtainPairSerializer, SetNewPasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import logging

logger = logging.getLogger(__name__)


class LoginView(TokenObtainPairView):
    """
    post:
    Obtain a new pair of access and refresh tokens.

    Request a pair of JWT tokens (access and refresh) by providing valid user credentials.

    Request Body:
    - username: string
    - password: string

    Responses:
    - 200: Token pair generated successfully
    - 400: Invalid credentials provided
    """
    serializer_class = CustomTokenObtainPairSerializer


class RegistrationView(generics.CreateAPIView):
    """
    post:
    Register a new user.

    Create a new user account. If a guarantor is provided, an activation email will be sent to the guarantor.
    Otherwise, a welcome email will be sent to the new user.

    Request Body:
    - email: string
    - password: string
    - guarantor: string (optional)
    - guarantor_email: string (optional)

    Responses:
    - 201: User registered successfully
    - 400: Guarantor does not exist or other validation errors
    """
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        """
        Handle user creation and email notifications.

        Create a new user. If a guarantor is specified, send an activation email to the guarantor.
        If the guarantor does not exist, notify the new user.
        If no guarantor is specified, send a welcome email to the new user.

        Parameters:
        - serializer: RegisterSerializer instance

        Raises:
        - serializers.ValidationError: If the guarantor does not exist
        """
        user_data = serializer.validated_data

        if user_data.get('guarantor'):
            guarantor_email = user_data.get('guarantor_email')
            try:
                guarantor_user = CustomUser.objects.get(email=guarantor_email)

                # Erlaubte Familien des Bürgen ermitteln
                allowed_families = {guarantor_user.family_1, guarantor_user.family_2}

                # Benutzer wählt mehrere Familien aus
                selected_families = user_data.get('selected_families', [])
                valid_families = [fam for fam in selected_families if fam in allowed_families]
                if not valid_families:
                    raise serializers.ValidationError({"detail":"Der Bürge ist für die ausgewählten Familien nicht berechtigt."})

                # Anpassen der Benutzer-Familienfelder basierend auf validierten Familien
                user_data['family_1'] = valid_families[0] if len(valid_families) > 0 else None
                user_data['family_2'] = valid_families[1] if len(valid_families) > 1 else None

                try:
                    user = serializer.save()
                except Exception as e:
                    logger.error(f'Fehler beim Speichern des Users: {e}', exc_info=True)
                    raise
                
                # Senden einer Aktivierungs-E-Mail an den Bürgen
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                activation_link = f"{settings.BACKEND_URL}/activate/{uidb64}/{token}/"

                subject = 'Bürgen für neuen Nutzer der Familienwebseite'
                html_message = render_to_string('guarantor_email.html', {'activation_link': activation_link, 'user': user, 'valid_families': valid_families})
                plain_message = strip_tags(html_message)
                from_email = settings.NO_REPLY_EMAIL
                to_email = [guarantor_user.email]

                email = EmailMultiAlternatives(subject, plain_message, from_email, to=to_email, reply_to=[settings.REPLY_TO_EMAIL])
                email.attach_alternative(html_message, "text/html")
                try:
                    email.send()
                except Exception as e:
                    logger.error(f"Senden der E-Mail fehlgeschlagen: {e}", exc_info=True)
                    raise serializers.ValidationError({"detail": "Fehler beim Versand der E-Mail. Bitte versuche es später erneut."})

            except CustomUser.DoesNotExist:
                # Senden einer Benachrichtigungs-E-Mail an den neuen Benutzer, dass der Bürge nicht existiert
                # subject = 'Ihr Bürge existiert nicht'
                # html_message = render_to_string('guarantor_not_exist_email.html', {'user': user_data})
                # plain_message = strip_tags(html_message)
                # from_email = settings.NO_REPLY_EMAIL
                # to_email = [user_data['email']]
# 
                # email = EmailMultiAlternatives(subject, plain_message, from_email, to=to_email, reply_to=[settings.REPLY_TO_EMAIL])
                # email.attach_alternative(html_message, "text/html")
                # email.send()
# 
                raise serializers.ValidationError({"detail": "Der angegebene Bürge existiert nicht."})
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
        """
        Handle the POST request for user registration.

        Validate the provided data, create the user, and send the respective email notification.

        Parameters:
        - request: The HTTP request object

        Responses:
        - 201: User registered successfully with email notification sent
        - 400: Validation error or other request issues
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'success': 'Please check the respective email.'}, status=status.HTTP_201_CREATED)


class ActivationView(APIView):
    """
    get:
    Activate a user account.

    Activate a user account using the provided UID and token.
    Sends confirmation emails to the user and guarantor (if applicable).

    Parameters:
    - uidb64: Base64 encoded user ID
    - token: Token for user activation

    Responses:
    - 302: Redirects to the frontend activation success or failure page
    """
    def get(self, request, uidb64, token):
        """
        Handle the GET request for account activation.

        Validate the UID and token, activate the user account, and send confirmation emails.

        Parameters:
        - request: The HTTP request object
        - uidb64: Base64 encoded user ID
        - token: Token for user activation

        Responses:
        - Redirects to the frontend activation success page if successful
        - Redirects to the frontend activation failure page if unsuccessful
        """
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
    """
    post:
    Request a password reset.

    Send a password reset link to the user's email address if the email is associated with an account.

    Request Body:
    - email: string

    Responses:
    - 200: Password reset link sent successfully
    - 400: User with the provided email does not exist
    """
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
    """
    post:
    Confirm a password reset.

    Reset the user's password using the provided UID and token, and set a new password.

    Request Body:
    - password: string

    Parameters:
    - uidb64: Base64 encoded user ID
    - token: Token for password reset

    Responses:
    - 200: Password reset successfully
    - 400: Invalid token, expired token, or other errors
    """
    def post(self, request, uidb64, token):
        """
        Handle the POST request for password reset confirmation.

        Validate the UID and token, set the new password for the user, and save it.

        Parameters:
        - request: The HTTP request object
        - uidb64: Base64 encoded user ID
        - token: Token for password reset

        Responses:
        - 200: Password reset successfully
        - 400: Invalid token, expired token, or other errors
        """
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


class BlacklistTokenView(APIView):
    """
    API view for blacklisting a refresh token.

    Processes a POST request containing a refresh token, which is then blacklisted to invalidate the token.
    Returns an HTTP 205 status code upon success, or an HTTP 400 status code if an error occurs.
    """
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """
    API view for changing a user's password.

    Processes a POST request with the old and new passwords.
    Returns an HTTP 200 status code with a success message if the password is changed successfully,
    or an HTTP 400 status code with error details if the provided data is invalid.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Passwort erfolgreich geändert."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeAuthorNameView(generics.UpdateAPIView):
    """
    API view that allows authenticated users to change their author name.
    Uses the ChangeAuthorNameSerializer for validation and updates the user profile.
    """
    serializer_class = ChangeAuthorNameSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Returns the current authenticated user.
        Ensures that the user can only update their own profile.
        """
        return self.request.user

    def update(self, request, *args, **kwargs):
        """
        Handles the update of the author's name. Validates the input data using the serializer,
        and if valid, saves the new name. Returns success response on successful update or error
        response if validation fails.
        """
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Author name updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeAlertPreferencesView(generics.UpdateAPIView):
    """
    API view that allows authenticated users to update their alert preferences.
    Uses the ChangeAlertPreferencesSerializer for validation and updates the user profile.
    """
    serializer_class = ChangeAlertPreferencesSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Returns the current authenticated user.
        Ensures that the user can only update their own profile.
        """
        return self.request.user

    def update(self, request, *args, **kwargs):
        """
        Handles the update of the user's alert preferences.
        Validates the input data using the serializer,
        and if valid, saves the new preferences. Returns success response on successful update
        or error response if validation fails.
        """
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Alert preferences updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnsubcribeAlerts(APIView):

    ALERT_VERBOSE_NAMES = {
        'faminfo': 'Familien-Informationen',
        'info': 'Allgemeine Informationen',
        'recipe': 'Rezepte',
        'discussion': 'Diskussionen',
    }

    def get(self, request, uidb64, token, alert_type):
        """
        Verarbeitet die Abmeldung von einem spezifischen Alert für einen Nutzer.
        """
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if alert_type == 'faminfo':
                user.alert_faminfo = False
            elif alert_type == 'info':
                user.alert_info = False
            elif alert_type == 'recipe':
                user.alert_recipe = False
            elif alert_type == 'discussion':
                user.alert_discussion = False
            user.save()

            verbose_name = self.ALERT_VERBOSE_NAMES.get(alert_type, 'Benachrichtigungen')
            
            return render(request, 'alerts/unsubscribe_confirmation.html', {
                'verbose_name': verbose_name
            })
        else:
            return render(request, 'alerts/unsubscribe_invalid.html')
    