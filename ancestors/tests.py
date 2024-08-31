from django.contrib.auth.models import Group
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Person, Relation
from accounts.models import CustomUser
from django.urls import reverse


class PersonListCreateViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_model = CustomUser

        self.user = self.user_model.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            username='testuser@example.com')
        self.user.is_active = True
        self.user.save()
        self.client.force_authenticate(user=self.user)

        # Create a group and assign it to the user
        group = Group.objects.create(name="Stammbaum Smith")
        self.user.groups.add(group)

        # Create Persons
        self.person1 = Person.objects.create(givn='John', surn='Smith', family_1='smith', confidential='none')
        self.person2 = Person.objects.create(givn='Jane', surn='Doe', family_1='smith', confidential='yes')
        self.person3 = Person.objects.create(givn='Alice', surn='Doe', family_1='smith', confidential='restricted')
        self.person4 = Person.objects.create(givn='Bob', surn='Johnson', family_1='johnson', confidential='none')

    def test_list_persons(self):
        """Test that the user can see persons related to their allowed family trees."""
        url = reverse('person-list-create')  # Use 'person-list-create' as the name of the URL
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_persons_confidential_yes(self):
        """Test that a person with confidential='yes' shows limited fields."""
        response = self.client.get('/api/ancestors/persons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Prüfe, ob vertrauliche Daten korrekt maskiert werden
        self.assertEqual(response.data[1]['name'], 'vertraulich')
        self.assertEqual(response.data[1]['surn'], '')
        self.assertEqual(response.data[1]['givn'], '')

    def test_list_persons_confidential_restricted(self):
        """Test that a person with confidential='restricted' shows partially restricted fields."""
        response = self.client.get('/api/ancestors/persons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Prüfe, ob eingeschränkt vertrauliche Daten korrekt angezeigt werden
        self.assertEqual(response.data[2]['name'], 'Alice Doe')
        self.assertEqual(response.data[2]['surn'], '')
        self.assertEqual(response.data[2]['givn'], '')

    def test_list_persons_excludes_non_related_families(self):
        """Test that persons from unrelated families are not included."""
        response = self.client.get('/api/ancestors/persons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Stelle sicher, dass Personen aus nicht verwandten Familien ausgeschlossen sind
        person_ids = [person['id'] for person in response.data]
        self.assertNotIn(self.person4.id, person_ids)


class PersonDetailViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_model = CustomUser

        self.user = self.user_model.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            username='testuser@example.com')
        self.user.is_active = True
        self.user.save()
        self.client.force_authenticate(user=self.user)

        # Create a group and assign it to the user
        group = Group.objects.create(name="Stammbaum Smith")
        self.user.groups.add(group)

        # Create a Person
        self.person1 = Person.objects.create(givn='John', surn='Smith', family_1='smith', confidential='none')
        self.person2 = Person.objects.create(givn='Jane', surn='Doe', family_1='smith', confidential='yes')
        self.person3 = Person.objects.create(givn='Alice', surn='Doe', family_1='smith', confidential='restricted')

    def test_retrieve_person_confidential_none(self):
        """Test retrieving a person with confidential='none' shows all fields."""
        response = self.client.get(f'/api/ancestors/persons/{self.person1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Smith')

    def test_retrieve_person_confidential_yes(self):
        """Test retrieving a person with confidential='yes' shows limited fields."""
        response = self.client.get(f'/api/ancestors/persons/{self.person2.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Prüfe, ob vertrauliche Daten korrekt maskiert werden
        self.assertEqual(response.data['name'], 'vertraulich')
        self.assertEqual(response.data['surn'], '')

    def test_retrieve_person_confidential_restricted(self):
        """Test retrieving a person with confidential='restricted' shows partially restricted fields."""
        response = self.client.get(f'/api/ancestors/persons/{self.person3.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Prüfe, ob eingeschränkt vertrauliche Daten korrekt angezeigt werden
        self.assertEqual(response.data['name'], 'Alice Doe')
        self.assertEqual(response.data['surn'], '')


class RelationListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_model = CustomUser

        # Erstelle einen Testbenutzer
        self.user = self.user_model.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            username='testuser@example.com'
        )
        self.user.is_active = True
        self.user.save()
        self.client.force_authenticate(user=self.user)

        # Erstelle eine Gruppe und füge den Benutzer hinzu
        group = Group.objects.create(name="Stammbaum Smith")
        self.user.groups.add(group)

        # Erstelle Person-Instanzen
        self.person1 = Person.objects.create(givn='John', surn='Smith', family_1='smith', confidential='none')
        self.person2 = Person.objects.create(givn='Jane', surn='Smith', family_1='smith', confidential='none')
        self.person3 = Person.objects.create(givn='Alice', surn='Doe', family_1='doe', confidential='none')
        self.person4 = Person.objects.create(givn='Bob', surn='Johnson', family_1='johnson', confidential='none')

        # Erstelle Relation-Instanzen
        self.relation1 = Relation.objects.create(person=self.person1, fath_refn=self.person2)
        self.relation2 = Relation.objects.create(person=self.person3, fath_refn=self.person4)

    def test_list_relations_for_related_family(self):
        """Test that relations for the user's allowed family trees are listed."""
        response = self.client.get('/api/ancestors/relations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Prüfe, ob die Beziehung für die Familie Smith enthalten ist
        relation_ids = [relation['id'] for relation in response.data]
        self.assertIn(self.relation1.id, relation_ids)

    def test_list_relations_excludes_unrelated_families(self):
        """Test that relations for unrelated families are not listed."""
        response = self.client.get('/api/ancestors/relations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Stelle sicher, dass die Beziehung für die Familie Doe/Johnson nicht enthalten ist
        relation_ids = [relation['id'] for relation in response.data]
        self.assertNotIn(self.relation2.id, relation_ids)


class RelationDetailViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_model = CustomUser

        # Erstelle einen Testbenutzer
        self.user = self.user_model.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            username='testuser@example.com'
        )
        self.user.is_active = True
        self.user.save()
        self.client.force_authenticate(user=self.user)

        # Erstelle eine Gruppe und füge den Benutzer hinzu
        group = Group.objects.create(name="Stammbaum Smith")
        self.user.groups.add(group)

        # Erstelle Person-Instanzen
        self.person1 = Person.objects.create(givn='John', surn='Smith', family_1='smith', confidential='none')
        self.person2 = Person.objects.create(givn='Jane', surn='Smith', family_1='smith', confidential='none')
        self.person3 = Person.objects.create(givn='Alice', surn='Doe', family_1='doe', confidential='none')

        # Erstelle Relation-Instanzen
        self.relation1 = Relation.objects.create(person=self.person1, fath_refn=self.person2)
        self.relation2 = Relation.objects.create(person=self.person3, fath_refn=None)

    def test_retrieve_relation_for_related_family(self):
        """Test retrieving a relation for the user's allowed family trees."""
        response = self.client.get(f'/api/ancestors/relations/{self.relation1.person.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['person'], self.person1.id)

    def test_retrieve_relation_for_unrelated_family(self):
        """Test that retrieving a relation for an unrelated family returns 404."""
        response = self.client.get(f'/api/ancestors/relations/{self.relation2.person.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
