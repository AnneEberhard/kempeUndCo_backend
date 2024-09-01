import json
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Recipe
from accounts.models import CustomUser
from django.contrib.auth.models import Group


class RecipeViewsTestCase(TestCase):
    def setUp(self):
        """
        Create test data for recipes and users.
        """
        self.client = APIClient()
        self.user_model = CustomUser

        self.user = self.user_model.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            username='testuser@example.com')
        self.user.is_active = True
        self.user.save()
        self.other_user = self.user_model.objects.create_user(
            email='otheruser@example.com',
            password='otherpassword',
            username='otheruser@example.com')
        self.other_user.is_active = True
        self.other_user.save()

        # Create recipes
        self.recipe1 = Recipe.objects.create(
            title='Recipe 1',
            content='Content for recipe 1',
            author=self.user,
            family_1='tree1'
        )
        self.recipe2 = Recipe.objects.create(
            title='Recipe 2',
            content='Content for recipe 2',
            author=self.other_user,
            family_1='tree2'
        )

        # URLs
        self.create_url = reverse('recipe-create')
        self.list_url = reverse('recipe-list')
        self.detail_url = reverse('recipe-detail', args=[self.recipe1.pk])

        group, created = Group.objects.get_or_create(name='Stammbaum Tree1')
        self.user.groups.add(group)  
        self.client.force_authenticate(user=self.user)

    def test_create_recipe(self):
        """
        Test creating a recipe with authenticated user.
        """
        data = {
            'title': 'New Recipe',
            'content': 'Content for new recipe',
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 3)
        self.assertEqual(Recipe.objects.latest('id').title, 'New Recipe')

    def test_list_recipes(self):
        """
        Test listing recipes based on allowed family trees.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        recipes = response.json()
        self.assertEqual(len(recipes), 1)  # Only one recipe should be returned for the user

    def test_detail_recipe(self):
        """
        Test retrieving the details of a specific recipe.
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Recipe 1')

    def test_update_recipe(self):
        """
        Test updating a recipe with image removal.
        """
        data = {
            'title': 'Updated Recipe 1',
            'content': 'Updated content',
            'deletedImages': json.dumps([]),  # Empty list of deleted images
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.recipe1.refresh_from_db()
        self.assertEqual(self.recipe1.title, 'Updated Recipe 1')

    def test_delete_recipe(self):
        """
        Test deleting a recipe.
        """
        delete_url = reverse('recipe-detail', args=[self.recipe1.pk])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.count(), 1)  # Only one recipe should remain

    def test_recipe_list_permissions(self):
        """
        Test that recipes from non-allowed family trees are not listed.
        """
        self.client.logout()
        data = {
            'email': 'otheruser@example.com',
            'password': 'otherpassword'
        }
        response = self.client.post('/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Set the token in the authorization header
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)  # The other user should not see recipes from the testuser's allowed family trees
