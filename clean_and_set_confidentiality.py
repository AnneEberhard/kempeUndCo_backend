import os
import django
import re
from datetime import datetime

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kempeUndCo_backend.settings')
django.setup()

from ancestors.models import Person

def is_valid_date(date_str):
    # Regex für das Datum im Format DD.MM.YYYY
    pattern = re.compile(r'\d{2}\.\d{2}\.\d{4}')
    if pattern.fullmatch(date_str):
        return True
    return False

def is_recent_birth_date(birth_date):
    # Überprüfen, ob das Geburtsdatum weniger als 120 Jahre zurückliegt
    birth_year = int(birth_date.split('.')[2])
    current_year = datetime.now().year
    return current_year - birth_year < 120

def transfer_invalid_dates_to_notes():
    persons = Person.objects.all()
    for person in persons:
        birth_date = person.birt_date
        death_date = person.deat_date
        notes_changed = False
        
        if birth_date and not is_valid_date(birth_date):
            person.note += f" Geburtsdatum: {birth_date}\n"
            person.birt_date = ''
            notes_changed = True
            
        if death_date and not is_valid_date(death_date):
            person.note += f" Todesdatum: {death_date}\n"
            person.deat_date = ''
            notes_changed = True
            
        if notes_changed:
            person.save()
            print(f"Transferred invalid dates for {person.givn} {person.surn}")

def set_confidentiality():
    persons = Person.objects.all()
    for person in persons:
        birth_date = person.birt_date
        death_date = person.deat_date
        
        if birth_date and is_valid_date(birth_date) and is_recent_birth_date(birth_date) and not death_date:
            person.confidential = 'restricted'
            person.save()
            print(f"Confidentiality for {person.givn} {person.surn} set to restricted")

if __name__ == "__main__":
    transfer_invalid_dates_to_notes()
    set_confidentiality()
