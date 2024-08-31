
from django.conf import settings
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from accounts.models import CustomUser


class LoginViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            username='testuser@example.com'
        )
        self.user.is_active = True
        self.user.save()
        self.login_url = '/login/'  # URL should match the path for `LoginView`

    def test_successful_login(self):
        """Test that login with correct credentials returns a token pair."""
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], self.user.email)
        self.assertEqual(response.data['user']['username'], self.user.username)

    def test_unsuccessful_login_wrong_password(self):
        """Test that login with incorrect password returns an error."""
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertIn('Invalid credentials', response.data['non_field_errors'])

    def test_unsuccessful_login_non_existent_user(self):
        """Test that login with a non-existent email returns an error."""
        data = {
            'email': 'nonexistentuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertIn('Invalid credentials', response.data['non_field_errors'])

    def test_unsuccessful_login_inactive_user(self):
        """Test that login with an inactive user returns an error."""
        self.user.is_active = False
        self.user.save()
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertIn('Inactive account', response.data['non_field_errors'])


class RegistrationViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.registration_url = '/register/'

    def test_successful_registration(self):
        """Test that user registration is successful."""
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'first_name': 'John',
            'last_name': 'Doe',
            'guarantor': False,
            'selected_families': ['family1']
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['success'], 'Please check the respective email.')

    def test_registration_with_guarantor(self):
        """Test that registration with a valid guarantor is successful."""
        # First, create a guarantor user
        guarantor = get_user_model().objects.create_user(
            email='guarantor@example.com',
            password='guarantorpassword',
            first_name='Guarantor',
            last_name='User',
            username='guarantor@example.com',
            family_1='family1'
        )
        guarantor.is_active = True
        guarantor.save()

        data = {
            'email': 'newuserwithguarantor@example.com',
            'password': 'newpassword',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'guarantor': True,
            'guarantor_email': 'guarantor@example.com',
            'selected_families': ['family1']
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['success'], 'Please check the respective email.')

    def test_registration_with_invalid_guarantor(self):
        """Test that registration with an invalid guarantor returns an error."""
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'first_name': 'John',
            'last_name': 'Doe',
            'guarantor': True,
            'guarantor_email': 'nonexistentguarantor@example.com',
            'selected_families': ['family1']
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_messages = [error for error in response.data]
        self.assertIn('Der angegebene Bürge existiert nicht.', error_messages)

    def test_registration_missing_required_fields(self):
        """Test that registration with missing required fields returns an error."""
        data = {
            'email': 'missingfield@example.com',
            'password': 'newpassword',
            # 'first_name': 'John',
            'last_name': 'Doe',
            'guarantor': False,
            'selected_families': ['family1']
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)
        self.assertIn('This field is required.', response.data['first_name'])


class ActivationViewTests(TestCase):
    def setUp(self):
        settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
        self.client = APIClient()
        self.user_model = get_user_model()

        # Create a test user
        self.user = self.user_model.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            guarantor=False
        )
        self.user.is_active = False
        self.user.save()

        # Generate activation token and UID
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)
        self.activation_url = reverse('activate', kwargs={'uidb64': self.uidb64, 'token': self.token})

    def test_successful_activation(self):
        """Test successful account activation."""
        response = self.client.get(self.activation_url)
        self.user.refresh_from_db()

        # Überprüfen, ob der Benutzer aktiviert wurde
        self.assertTrue(self.user.is_active)

        # Überprüfen, ob die Weiterleitung zur korrekten Seite erfolgt
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIn(f"{settings.FRONTEND_URL}/activation-success", response.url)

        # Überprüfen, ob E-Mails gesendet wurden
        email_messages = mail.outbox
        self.assertEqual(len(email_messages), 1)
        self.assertIn('Konto wurde aktiviert', email_messages[0].subject)

    def test_activation_invalid_token(self):
        """Test activation with invalid token."""
        invalid_token = 'invalid_token'
        invalid_activation_url = reverse('activate', kwargs={'uidb64': self.uidb64, 'token': invalid_token})
        response = self.client.get(invalid_activation_url)

        # Überprüfen, ob der Benutzer nicht aktiviert wurde
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

        # Überprüfen, ob die Weiterleitung zur Fehlerseite erfolgt
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIn(f"{settings.FRONTEND_URL}/activation-failure", response.url)

        # Überprüfen, dass keine E-Mails gesendet wurden
        email_messages = mail.outbox
        self.assertEqual(len(email_messages), 0)

    def test_activation_invalid_uid(self):
        """Test activation with invalid UID."""
        invalid_uidb64 = urlsafe_base64_encode(force_bytes(9999))  # Non-existent user ID
        invalid_activation_url = reverse('activate', kwargs={'uidb64': invalid_uidb64, 'token': self.token})
        response = self.client.get(invalid_activation_url)

        # Überprüfen, ob der Benutzer nicht aktiviert wurde
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

        # Überprüfen, ob die Weiterleitung zur Fehlerseite erfolgt
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIn(f"{settings.FRONTEND_URL}/activation-failure", response.url)

        # Überprüfen, dass keine E-Mails gesendet wurden
        email_messages = mail.outbox
        self.assertEqual(len(email_messages), 0)

    def test_activation_with_guarantor(self):
        """Test activation for a user with a guarantor."""
        # Create a guarantor
        guarantor = self.user_model.objects.create_user(
            email='guarantor@example.com',
            password='guarantorpassword',
            first_name='Guarantor',
            last_name='User',
            username='guarantor@example.com'
        )
        self.user.guarantor = True
        self.user.guarantor_email = 'guarantor@example.com'
        self.user.save()

        response = self.client.get(self.activation_url)
        self.user.refresh_from_db()

        # Überprüfen, ob der Benutzer aktiviert wurde
        self.assertTrue(self.user.is_active)

        # Überprüfen, ob die Weiterleitung zur Erfolgsseite erfolgt
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIn(f"{settings.FRONTEND_URL}/activation-success", response.url)

        # Überprüfen, dass zwei E-Mails gesendet wurden (eine an den Benutzer, eine an den Bürgen)
        email_messages = mail.outbox
        self.assertEqual(len(email_messages), 2)
        self.assertIn('Konto wurde aktiviert', email_messages[0].subject)
        self.assertIn('Ein neuer Benutzer wurde aktiviert', email_messages[1].subject)

    def test_activation_missing_user(self):
        """Test activation when user does not exist."""
        # Create a URL with an invalid user ID
        invalid_uidb64 = urlsafe_base64_encode(force_bytes(9999))  # Non-existent user ID
        invalid_activation_url = reverse('activate', kwargs={'uidb64': invalid_uidb64, 'token': self.token})
        response = self.client.get(invalid_activation_url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIn(f"{settings.FRONTEND_URL}/activation-failure", response.url)


class PasswordResetRequestViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_model = CustomUser

        self.user = self.user_model.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )
        self.user.is_active = True
        self.user.save()
        self.password_reset_url = reverse('password_reset_request')

    def test_password_reset_request_success(self):
        """Test successful password reset request."""
        data = {'email': 'testuser@example.com'}
        response = self.client.post(self.password_reset_url, data, format='json')

        # Überprüfen, ob der Statuscode 200 OK ist
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Überprüfen, dass eine E-Mail gesendet wurde
        email_messages = mail.outbox
        self.assertEqual(len(email_messages), 1)
        self.assertIn('Passwort zurücksetzen', email_messages[0].subject)

    def test_password_reset_request_invalid_email(self):
        """Test password reset request with an invalid email."""
        data = {'email': 'invaliduser@example.com'}
        response = self.client.post(self.password_reset_url, data, format='json')

        # Überprüfen, ob der Statuscode 400 Bad Request ist
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Überprüfen, dass keine E-Mails gesendet wurden
        email_messages = mail.outbox
        self.assertEqual(len(email_messages), 0)


class PasswordResetConfirmViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_model = CustomUser

        # Create a test user
        self.user = self.user_model.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )
        self.user.is_active = True
        self.user.save()
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)
        self.password_reset_confirm_url = reverse('password_reset_confirm', kwargs={'uidb64': self.uidb64, 'token': self.token})

    def test_password_reset_confirm_success(self):
        """Test successful password reset confirmation."""
        data = {'password': 'newpassword'}
        response = self.client.post(self.password_reset_confirm_url, data, format='json')

        # Überprüfen, ob der Statuscode 200 OK ist
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Überprüfen, ob das Passwort erfolgreich geändert wurde
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword'))

    def test_password_reset_confirm_invalid_token(self):
        """Test password reset confirmation with an invalid token."""
        invalid_token_url = reverse('password_reset_confirm', kwargs={'uidb64': self.uidb64, 'token': 'invalidtoken'})
        data = {'password': 'newpassword'}
        response = self.client.post(invalid_token_url, data, format='json')

        # Überprüfen, ob der Statuscode 400 Bad Request ist
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Überprüfen, ob das Passwort nicht geändert wurde
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password('newpassword'))

    def test_password_reset_confirm_invalid_uid(self):
        """Test password reset confirmation with an invalid UID."""
        invalid_uid = urlsafe_base64_encode(force_bytes(9999))  # Non-existent user ID
        invalid_uid_url = reverse('password_reset_confirm', kwargs={'uidb64': invalid_uid, 'token': self.token})
        data = {'password': 'newpassword'}
        response = self.client.post(invalid_uid_url, data, format='json')

        # Überprüfen, ob der Statuscode 400 Bad Request ist
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Überprüfen, ob das Passwort nicht geändert wurde
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password('newpassword'))
