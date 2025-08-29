import json
import os
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer


class RecipeCreateView(APIView):
    """
    View to create a new Recipe.

    Only authenticated users are allowed to create recipes. The view automatically sets
    the `family_1` and `family_2` fields based on the logged-in user's family trees.

    **URL:** `/recipes/`
    **Method:** `POST`
    """
    def post(self, request, *args, **kwargs):
        user = request.user
        family_1 = user.family_1
        family_2 = user.family_2

        data = request.data.copy()
        data['family_1'] = family_1
        data['family_2'] = family_2

        serializer = RecipeSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeListView(generics.ListAPIView):
    """
    View to list all Recipes accessible to the current user.

    The recipes are filtered based on the allowed family trees for the logged-in user. Only
    recipes where `family_1` or `family_2` matches the allowed family trees are returned.

    **URL:** `/recipes/`
    **Method:** `GET`
    """
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def get_allowed_families(self):
        """
        Get the allowed family names for the current user.

        **Returns:**
        - A set of allowed family names based on the groups the user belongs to.
        """
        user = self.request.user
        allowed_families = set()

        if user.family_1:
            allowed_families.add(user.family_1.lower())
        if user.family_2:
            allowed_families.add(user.family_2.lower())

        return allowed_families

    def get_queryset(self):
        """
        Filter recipes based on the allowed family trees for the current user.

        **Returns:**
        - A queryset of recipes where `family_1` or `family_2` is in the allowed family trees.
        """
        allowed_families = self.get_allowed_families()
        if not allowed_families:
            return Recipe.objects.none()

        return Recipe.objects.filter(
            Q(family_1__in=allowed_families) | Q(family_2__in=allowed_families)
        ).distinct()


class RecipeDetailView(APIView):
    """
    View to retrieve, update, or delete a specific Recipe.

    **URL:** `/recipes/<pk>/`
    **Methods:** `GET`, `PUT`, `DELETE`
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        """
        Retrieve the details of a specific recipe.

        **URL Parameter:**
        - `pk`: The primary key of the recipe to retrieve.

        **Returns:**
        - The details of the requested recipe in JSON format.
        """
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = RecipeSerializer(recipe, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        """
        Update a specific recipe, including handling image removal.

        **URL Parameter:**
        - `pk`: The primary key of the recipe to update.

        **Request Data:**
        - `deletedImages`: JSON-encoded list of images to remove.

        **Returns:**
        - The updated recipe data in JSON format if the update is successful.
        """
        recipe = get_object_or_404(Recipe, pk=pk)
        # deleted_images = json.loads(request.data.get('deletedImages', '[]'))

        for field in ['image_1', 'image_2', 'image_3', 'image_4']:
            if field in request.data and request.data[field] == '':
                image_field = getattr(recipe, field, None)
                if image_field:
                    if os.path.isfile(image_field.path):
                        os.remove(image_field.path)
                    setattr(recipe, field, None)

                thumbnail_field = f'{field}_thumbnail'
                thumbnail = getattr(recipe, thumbnail_field, None)
                if thumbnail and os.path.isfile(thumbnail.path):
                    os.remove(thumbnail.path)
                    setattr(recipe, thumbnail_field, None)

        for field in ['pdf_1', 'pdf_2', 'pdf_3', 'pdf_4']:
            if field in request.data and request.data[field] == '':
                pdf_field = getattr(recipe, field, None)
                if pdf_field and os.path.isfile(pdf_field.path):
                    os.remove(pdf_field.path)
                    setattr(recipe, field, None)

                # optional auch den Namen löschen
                name_field = f'{field}_name'
                if hasattr(recipe, name_field):
                    setattr(recipe, name_field, '')

        serializer = RecipeSerializer(recipe, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
        Delete a specific recipe.

        **URL Parameter:**
        - `pk`: The primary key of the recipe to delete.

        **Returns:**
        - HTTP status code 204 No Content if the deletion is successful.
        """
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
