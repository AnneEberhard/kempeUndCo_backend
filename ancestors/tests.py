from django.contrib.auth.models import Group, User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Person, Relation


class PersonListCreateViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        # Create a group and assign it to the user
        group = Group.objects.create(name="Stammbaum Smith")
        self.user.groups.add(group)

        # Create Persons
        self.person1 = Person.objects.create(name='John Smith', family_1='smith')
        self.person2 = Person.objects.create(name='Jane Doe', family_1='doe')

    def test_list_persons(self):
        """Test that the user can see persons related to their allowed family trees."""
        response = self.client.get('/persons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one person should be visible

    def test_create_person(self):
        """Test creating a new person."""
        data = {'name': 'Alice Smith', 'family_1': 'smith'}
        response = self.client.post('/persons/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Person.objects.count(), 3)
        self.assertEqual(response.data['name'], 'Alice Smith')


class PersonDetailViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        # Create a group and assign it to the user
        group = Group.objects.create(name="Stammbaum Smith")
        self.user.groups.add(group)

        # Create a Person
        self.person = Person.objects.create(name='John Smith', family_1='smith')

    def test_retrieve_person(self):
        """Test retrieving a person detail."""
        response = self.client.get(f'/persons/{self.person.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.person.name)

    def test_update_person(self):
        """Test updating a person."""
        data = {'name': 'Updated Name'}
        response = self.client.put(f'/persons/{self.person.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.person.refresh_from_db()
        self.assertEqual(self.person.name, 'Updated Name')

    def test_delete_person(self):
        """Test deleting a person."""
        response = self.client.delete(f'/persons/{self.person.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Person.objects.count(), 0)


class RelationListCreateViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        # Create a group and assign it to the user
        group = Group.objects.create(name="Stammbaum Smith")
        self.user.groups.add(group)

        # Create Persons and Relations
        self.person1 = Person.objects.create(name='John Smith', family_1='smith')
        self.person2 = Person.objects.create(name='Jane Doe', family_1='doe')

    def test_list_relations(self):
        """Test that the user can see relations related to their allowed family trees."""
        response = self.client.get('/relations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming relations have been created, check the count
        self.assertEqual(len(response.data), 0)  # No relations if none were added

    def test_create_relation(self):
        """Test creating a new relation."""
        data = {
            'person': self.person1.id,
            'related_person': self.person2.id,
            # Add any other necessary relation fields
        }
        response = self.client.post('/relations/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Relation.objects.count(), 1)
        self.assertEqual(response.data['person'], self.person1.id)


class RelationDetailViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        # Create a group and assign it to the user
        group = Group.objects.create(name="Stammbaum Smith")
        self.user.groups.add(group)

        # Create a Person and a Relation
        self.person1 = Person.objects.create(name='John Smith', family_1='smith')
        self.person2 = Person.objects.create(name='Jane Doe', family_1='doe')
        self.relation = Relation.objects.create(person=self.person1, related_person=self.person2)

    def test_retrieve_relation(self):
        """Test retrieving a relation detail."""
        response = self.client.get(f'/relations/{self.relation.person_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['person'], self.relation.person_id)

    def test_update_relation(self):
        """Test updating a relation."""
        data = {'related_person': self.person1.id}  # Swap the relation
        response = self.client.put(f'/relations/{self.relation.person_id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.relation.refresh_from_db()
        self.assertEqual(self.relation.related_person.id, self.person1.id)

    def test_delete_relation(self):
        """Test deleting a relation."""
        response = self.client.delete(f'/relations/{self.relation.person_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Relation.objects.count(), 0)
