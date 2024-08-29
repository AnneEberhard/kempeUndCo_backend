import json
import os
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from infos.models import Info
from infos.serializers import InfoSerializer


class InfoCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Hole die family_1 und family_2 des angemeldeten Benutzers
        user = request.user
        print(user.family_1)
        family_1 = user.family_1
        family_2 = user.family_2

        # Erstelle die Daten für den Serializer und füge family_1 und family_2 hinzu
        data = request.data.copy()
        data['family_1'] = family_1
        data['family_2'] = family_2

        serializer = InfoSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InfoListView(generics.ListAPIView):
    serializer_class = InfoSerializer
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
        """Filtert die Infos basierend auf den erlaubten Stammbaum-Namen des Benutzers."""
        allowed_family_trees = self.get_allowed_family_trees()
        if not allowed_family_trees:
            return Info.objects.none()  # Keine Infos zurückgeben, wenn keine erlaubten Stammbäume vorhanden sind

        return Info.objects.filter(
            Q(family_1__in=allowed_family_trees) |
            Q(family_2__in=allowed_family_trees)
        ).distinct()


class InfoDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, *args, **kwargs):
        info = get_object_or_404(Info, pk=pk)
        serializer = InfoSerializer(info, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        info = get_object_or_404(Info, pk=pk)
        deleted_images = json.loads(request.data.get('deletedImages', '[]'))

        for field in ['image_1', 'image_2', 'image_3', 'image_4']:
            if field in request.data and request.data[field] == '':
                image_field = getattr(info, field, None)
                if image_field:
                    if os.path.isfile(image_field.path):
                        os.remove(image_field.path)
                    setattr(info, field, None)

        serializer = InfoSerializer(info, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        info = get_object_or_404(Info, pk=pk)
        info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
