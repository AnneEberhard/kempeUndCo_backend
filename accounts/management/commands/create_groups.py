from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from kempeUndCo_backend.constants import FAMILIES

class Command(BaseCommand):
    help = 'Create groups for family trees'

    def handle(self, *args, **options):

        for family in FAMILIES:
            group_name = f"Stammbaum {family.capitalize()}"
            Group.objects.get_or_create(name=group_name)
        self.stdout.write(self.style.SUCCESS('Groups created successfully.'))

