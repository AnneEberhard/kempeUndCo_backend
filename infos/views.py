import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView

from infos.models import Info
from infos.serializers import InfoSerializer

@api_view(['DELETE'])
def delete_image(request, Info_id, image_field):
    try:
        Info = Info.objects.get(id=Info_id)
        image = getattr(Info, image_field)
        if image and os.path.isfile(image.path):
            os.remove(image.path)
            setattr(Info, image_field, None)
            Info.save()
            return Response({'message': 'Image deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
    except Info.DoesNotExist:
        return Response({'error': 'Info not found'}, status=status.HTTP_404_NOT_FOUND)


class InfoCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = InfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InfoListView(generics.ListAPIView):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer


class InfoDetailView(generics.RetrieveAPIView):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer
