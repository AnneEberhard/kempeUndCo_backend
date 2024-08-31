from django.contrib.auth.models import Group, User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from ancestors.models import Person
from .models import Discussion, DiscussionEntry
from .serializers import DiscussionSerializer, DiscussionEntrySerializer


class DiscussionListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        # Create groups and assign to the user
        group = Group.objects.create(name="Stammbaum Smith")
        self.user.groups.add(group)

        # Create Persons and Discussions
        self.person1 = Person.objects.create(name='John Smith', family_1='smith')
        self.discussion1 = Discussion.objects.create(person=self.person1)

    def test_list_discussions(self):
        """Test that the user can see discussions related to their allowed family trees."""
        response = self.client.get('/discussions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one discussion should be visible

    def test_no_access_to_other_families(self):
        """Test that the user cannot see discussions related to other families."""
        # Create a person in a different family and add a discussion
        other_person = Person.objects.create(name='Jane Doe', family_1='doe')
        Discussion.objects.create(person=other_person)

        response = self.client.get('/discussions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Still only one discussion visible


class GetOrCreateDiscussionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        # Create a person
        self.person = Person.objects.create(name='John Smith')

    def test_get_existing_discussion(self):
        """Test retrieving an existing discussion."""
        discussion = Discussion.objects.create(person=self.person)
        response = self.client.get(f'/discussions/{self.person.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], discussion.id)

    def test_create_new_discussion(self):
        """Test creating a new discussion for a person without one."""
        response = self.client.post(f'/discussions/{self.person.id}/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Discussion.objects.count(), 1)
        self.assertEqual(response.data['person']['id'], self.person.id)


class CreateDiscussionEntryViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        # Create a person and a discussion
        self.person = Person.objects.create(name='John Smith')
        self.discussion = Discussion.objects.create(person=self.person)

    def test_create_entry(self):
        """Test creating a discussion entry."""
        data = {
            'discussion': self.discussion.id,
            'title': 'Test Entry',
            'content': 'This is a test entry.'
        }
        response = self.client.post('/discussion-entries/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DiscussionEntry.objects.count(), 1)
        self.assertEqual(DiscussionEntry.objects.get().author, self.user)


class DiscussionEntryDetailViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        # Create a person, discussion, and entry
        self.person = Person.objects.create(name='John Smith')
        self.discussion = Discussion.objects.create(person=self.person)
        self.entry = DiscussionEntry.objects.create(
            discussion=self.discussion,
            author=self.user,
            title='Original Title',
            content='Original content.'
        )

    def test_get_entry(self):
        """Test retrieving a discussion entry."""
        response = self.client.get(f'/discussion-entries/{self.entry.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.entry.title)

    def test_update_entry(self):
        """Test updating a discussion entry."""
        data = {'title': 'Updated Title'}
        response = self.client.put(f'/discussion-entries/{self.entry.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.title, 'Updated Title')

    def test_delete_entry(self):
        """Test deleting a discussion entry."""
        response = self.client.delete(f'/discussion-entries/{self.entry.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(DiscussionEntry.objects.count(), 0)


class DiscussionDetailCreateViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        # Create a person
        self.person = Person.objects.create(name='John Smith')

    def test_get_nonexistent_discussion(self):
        """Test trying to retrieve a discussion that does not exist."""
        response = self.client.get(f'/discussions/{self.person.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_discussion(self):
        """Test creating a discussion for a person."""
        response = self.client.post(f'/discussions/{self.person.id}/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Discussion.objects.count(), 1)
        self.assertEqual(response.data['person']['id'], self.person.id)
