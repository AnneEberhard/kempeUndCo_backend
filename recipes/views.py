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
    def post(self, request, *args, **kwargs):
        user = request.user
        print(user.family_1)
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
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def get_allowed_family_trees(self):
        """Holt die erlaubten Stammbaum-Namen für den aktuellen Benutzer."""
        user = self.request.user
        allowed_trees = set()

        # Sammle alle Stammbäume, die der Benutzer sehen darf
        for group in user.groups.all():
            if group.name.startswith("Stammbaum "):
                tree_name = group.name.replace("Stammbaum ", "").lower()
                allowed_trees.add(tree_name)
        
        return allowed_trees

    def get_queryset(self):
        """Filtert die Rezepte basierend auf den erlaubten Stammbaum-Namen des Benutzers."""
        allowed_family_trees = self.get_allowed_family_trees()
        if not allowed_family_trees:
            return Recipe.objects.none()  # Keine Rezepte zurückgeben, wenn keine erlaubten Stammbäume vorhanden sind

        return Recipe.objects.filter(
            Q(family_1__in=allowed_family_trees) |
            Q(family_2__in=allowed_family_trees)
        ).distinct()


class RecipeDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = RecipeSerializer(recipe, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=pk)
        deleted_images = json.loads(request.data.get('deletedImages', '[]'))

        for field in ['image_1', 'image_2', 'image_3', 'image_4']:
            if field in request.data and request.data[field] == '':
                image_field = getattr(recipe, field, None)
                if image_field:
                    if os.path.isfile(image_field.path):
                        os.remove(image_field.path)
                    setattr(recipe, field, None)

        serializer = RecipeSerializer(recipe, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)