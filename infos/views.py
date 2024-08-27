import json
import os
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView

from infos.models import Info
from infos.serializers import InfoSerializer


class InfoCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = InfoSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InfoListView(generics.ListAPIView):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer


class InfoDetailView(APIView):
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
