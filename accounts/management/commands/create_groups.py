from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Create groups for family trees'

    def handle(self, *args, **options):
        family_tree_choices = ['kempe', 'huenten']  # Weitere Stammbäume hinzufügen, falls nötig
        for tree in family_tree_choices:
            group_name = f"Stammbaum {tree.capitalize()}"
            Group.objects.get_or_create(name=group_name)
        self.stdout.write(self.style.SUCCESS('Groups created successfully.'))

