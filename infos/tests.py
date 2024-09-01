from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import Group
from .models import Info
from accounts.models import CustomUser


class InfoTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_model = CustomUser

        self.user = self.user_model.objects.create_user(
            username='testuser',
            email="testuser@example.com",
            password='testpassword'
        )
        self.user.is_active = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        group, created = Group.objects.get_or_create(name='Stammbaum Kempe')
        self.user.groups.add(group)        
        
        # Create an Info instance
        self.info = Info.objects.create(
            title='Test Info',
            content='This is a test info.',
            family_1='kempe',
            author=self.user
        )
        self.info_url = reverse('info-detail', args=[self.info.pk])
        self.create_url = reverse('info-create')
        self.list_url = reverse('info-list')

    def test_create_info(self):
        """
        Test creating a new Info instance.
        """
        data = {
            'title': 'New Info',
            'content': 'Content for new info',
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Info.objects.count(), 2)
        self.assertEqual(Info.objects.get(pk=response.data['id']).title, 'New Info')

    def test_list_info(self):
        """
        Test listing Info instances with filtering based on allowed family trees.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Info')

    def test_retrieve_info(self):
        """
        Test retrieving a single Info instance.
        """
        response = self.client.get(self.info_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Info')

    def test_update_info(self):
        """
        Test updating an existing Info instance.
        """
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Updated Info',
            'content': 'Updated content',
        }
        response = self.client.put(self.info_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Info.objects.get(pk=self.info.pk).title, 'Updated Info')

    def test_delete_info(self):
        """
        Test deleting an Info instance.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.info_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Info.objects.count(), 0)

    def test_info_create_without_authentication(self):
        """
        Test creating an Info instance without authentication.
        """
        self.client.force_authenticate(user=None)
        data = {
            'title': 'Unauthorized Info',
            'content': 'Content for unauthorized info',
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
