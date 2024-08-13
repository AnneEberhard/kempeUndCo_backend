import os
import django
from datetime import datetime

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kempeUndCo_backend.settings')
django.setup()

from ancestors.models import Person


def migrate_dates():
    for person in Person.objects.all():
        if person.birt_date:
            try:
                birth_date = datetime.strptime(person.birt_date, '%d.%m.%Y').date()
                person.birth_date_formatted = birth_date
            except ValueError:
                print(f"Invalid birth date format for person {person.id}: {person.birt_date}")
        if person.deat_date:
            try:
                death_date = datetime.strptime(person.deat_date, '%d.%m.%Y').date()
                person.death_date_formatted = death_date
            except ValueError:
                print(f"Invalid death date format for person {person.id}: {person.deat_date}")
        person.save()


migrate_dates()
