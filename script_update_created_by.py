import os
import django

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kempeUndCo_backend.settings')
django.setup()

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model 
from ancestors.models import Person


def update_created_by(username):
    User = get_user_model()  # Hole das benutzerdefinierte User-Modell (weil CustomUser!)
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        print(f"Benutzer '{username}' existiert nicht.")
        return

    # Alle Personen-Datensätze aktualisieren, deren `created_by` noch leer ist
    updated_count = Person.objects.filter(created_by__isnull=True).update(created_by=user)

    print(f'Erfolgreich {updated_count} Datensätze aktualisiert.')

if __name__ == "__main__":
    # Hier den Benutzernamen des Erstellers angeben
    target_username = 'admin'  # Cave: dieser user muss existieren!
    update_created_by(target_username)
