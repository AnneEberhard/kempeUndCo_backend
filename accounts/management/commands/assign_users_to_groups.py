from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

from accounts.models import CustomUser
from kempeUndCo_backend.constants import FAMILIES


class Command(BaseCommand):
    help = 'Assign existing users to groups based on their family_1/2 values'

    def handle(self, *args, **options):
        users_assigned = 0
        for user in CustomUser.objects.all():
            # Lösche alle bestehenden Gruppenmitgliedschaften
            user.groups.clear()
            families = {user.family_1, user.family_2}
            for family in families:
                if family:
                    group_name = f"Stammbaum {family.capitalize()}"
                    group, created = Group.objects.get_or_create(name=group_name)
                    user.groups.add(group)
                    users_assigned += 1
        
        self.stdout.write(self.style.SUCCESS(f'{users_assigned} users were successfully assigned to groups.'))
