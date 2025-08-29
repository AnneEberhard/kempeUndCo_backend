import json
import os
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from django.contrib.auth.models import Group

from famInfos.models import FamInfo
from famInfos.serializers import FamInfoSerializer


class FamInfoCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Creates a new famInfo instance with `family_1` and `family_2` fields populated from the current user.

        If the user is authenticated, `family_1` and `family_2` from the user are added to the request data before
        saving a new famInfo instance. If the request data is valid, the famInfo instance is created and returned with
        a 201 Created status. Otherwise, a 400 Bad Request status is returned with validation errors.

        Args:
            request: The HTTP request object containing data to create a new famInfo instance.

        Returns:
            Response: The API response containing the created famInfo instance or validation errors.
        """
        data = request.data.copy()

        serializer = FamInfoSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FamInfoListView(generics.ListAPIView):
    serializer_class = FamInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_allowed_families(self):
        """
        Retrieves the allowed family tree names for the current user .

        Returns:
            set: A set of allowed family names for the current user.
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
        Filters famInfo instances based on the allowed family tree names of the user.

        The method filters the famInfo instances to include only those related to the family trees the user has access to.
        If no allowed family trees are found, an empty queryset is returned.

        Returns:
            QuerySet: A queryset of famInfo instances filtered by allowed family trees.
        """
        allowed_families = self.get_allowed_families()
        if not allowed_families:
            return FamInfo.objects.none()

        queryset = FamInfo.objects.filter(Q(family_1__in=allowed_families) | Q(family_2__in=allowed_families)).distinct()

        return queryset


class FamInfoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        """
        Retrieves the details of a specific famInfo instance.

        Args:
            request: The HTTP request object.
            pk: The primary key of the famInfo instance to retrieve.

        Returns:
            Response: The API response containing the famInfo details or a 404 Not Found status if the famInfo instance does not exist.
        """
        famInfo = get_object_or_404(famInfo, pk=pk)
        serializer = FamInfoSerializer(famInfo, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        """
        Updates a specific famInfo instance.

        The method supports partial updates. If image fields are cleared in the request data, the corresponding images are deleted.

        Args:
            request: The HTTP request object containing data to update the famInfo instance.
            pk: The primary key of the famInfo instance to update.

        Returns:
            Response: The API response containing the updated famInfo instance or validation errors, or a 404 Not Found status if the famInfo instance does not exist.
        """
        famInfo = get_object_or_404(FamInfo, pk=pk)

        for field in ['image_1', 'image_2', 'image_3', 'image_4']:
            if field in request.data and request.data[field] == '':
                image_field = getattr(famInfo, field, None)
                if image_field:
                    if os.path.isfile(image_field.path):
                        os.remove(image_field.path)
                        setattr(famInfo, field, None)

                thumbnail_field = f'{field}_thumbnail'
                thumbnail = getattr(famInfo, thumbnail_field, None)
                if thumbnail and os.path.isfile(thumbnail.path):
                    os.remove(thumbnail.path)
                    setattr(famInfo, thumbnail_field, None)

        for field in ['pdf_1', 'pdf_2', 'pdf_3', 'pdf_4']:
            if field in request.data and request.data[field] == '':
                pdf_field = getattr(famInfo, field, None)
                if pdf_field and os.path.isfile(pdf_field.path):
                    os.remove(pdf_field.path)
                    setattr(famInfo, field, None)

                # optional auch den Namen löschen
                name_field = f'{field}_name'
                if hasattr(famInfo, name_field):
                    setattr(famInfo, name_field, '')

        serializer = FamInfoSerializer(famInfo, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
        Deletes a specific famInfo instance.

        Args:
            request: The HTTP request object.
            pk: The primary key of the famInfo instance to delete.

        Returns:
            Response: A 204 No Content response if the famInfo instance was deleted, or a 404 Not Found status if the famInfo instance does not exist.
        """
        famInfo = get_object_or_404(FamInfo, pk=pk)
        famInfo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
