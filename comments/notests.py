from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.reverse import reverse


class CommentCreateViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            username='testuser@example.com')
        self.client.login(email='testuser@example.com', password='testpassword')
        self.url = reverse('comment-create')  # Adjust if using a different URL name

    def test_create_comment(self):
        data = {
            'info_id': 1,
            'recipe_id': 1,
            'content': 'This is a test comment'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, 'This is a test comment')
        self.assertEqual(Comment.objects.get().author, self.user)


class CommentListViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            username='testuser@example.com')
        self.client.login(email='testuser@example.com', password='testpassword')
        self.url = reverse('comment-list')  # Adjust if using a different URL name
        self.comment1 = Comment.objects.create(info_id=1, recipe_id=1, content='Comment 1', author=self.user)
        self.comment2 = Comment.objects.create(info_id=2, recipe_id=2, content='Comment 2', author=self.user)

    def test_list_all_comments(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_info_id(self):
        response = self.client.get(self.url, {'info': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], 'Comment 1')

    def test_filter_by_recipe_id(self):
        response = self.client.get(self.url, {'recipe': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], 'Comment 2')


class CommentDetailViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            username='testuser@example.com')
        self.client.login(email='testuser@example.com', password='testpassword')
        self.comment = Comment.objects.create(info_id=1, recipe_id=1, content='Detail Comment', author=self.user)
        self.url = reverse('comment-detail', args=[self.comment.pk])  # Adjust if using a different URL name

    def test_get_comment(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Detail Comment')

    def test_update_comment(self):
        data = {'content': 'Updated Comment'}
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Updated Comment')

    def test_delete_comment(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)
