import json
import os
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer


class RecipeCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RecipeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeListView(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeDetailView(APIView):
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