from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from infos.models import Info
from recipes.models import Recipe
from .models import Comment
from rest_framework.reverse import reverse
from accounts.models import CustomUser


class CommentCreateViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_model = CustomUser

        self.user = self.user_model.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            username='testuser@example.com')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('comment-create')  # Adjust if using a different URL name

    def test_create_comment(self):
        data = {
            'info_id': 1,
            'content': 'This is a test comment'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, 'This is a test comment')
        self.assertEqual(Comment.objects.get().author, self.user)


class CommentListViewTests(TestCase):
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

        self.url = reverse('comment-list')  # Adjust if using a different URL name

        self.recipe1 = Recipe.objects.create(
            title='Recipe 1',
            content='Content for recipe 1',
            author=self.user
        )
        self.recipe2 = Recipe.objects.create(
            title='Recipe 2',
            content='Content for recipe 2',
            author=self.user
        )
        self.info1 = Info.objects.create(
            title='Info 1',
            content='Content for Info 1',
            author=self.user
        )

        self.comment1 = Comment.objects.create(recipe_id=1, content='Comment 1', author=self.user)
        self.comment2 = Comment.objects.create(recipe_id=2, content='Comment 2', author=self.user)
        self.comment3 = Comment.objects.create(info_id=1, content='Comment Info', author=self.user)

    def test_list_all_comments(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_by_recipe_id(self):
        response = self.client.get(self.url, {'recipe': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], 'Comment 1')

    def test_filter_by_info_id(self):
        response = self.client.get(self.url, {'info': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], 'Comment Info')


class CommentDetailViewTests(TestCase):
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

        self.info1 = Info.objects.create(
            title='Info 1',
            content='Content for Info 1',
            author=self.user
        )

        self.comment = Comment.objects.create(info_id=1, content='Detail Comment', author=self.user)
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
