from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ancestors.models import Person
from .models import Discussion
from .serializers import DiscussionEntrySerializer, DiscussionSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_discussions(request):
    discussions = Discussion.objects.all()
    serializer = DiscussionSerializer(discussions, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_or_create_discussion(request, id):
    try:
        person = Person.objects.get(id=id)
    except Person.DoesNotExist:
        return Response({'error': 'Person not found'}, status=404)

    discussion, created = Discussion.objects.get_or_create(person=person)
    serializer = DiscussionSerializer(discussion)

    return Response(serializer.data, status=201 if created else 200)


class CreateDiscussionEntryView(APIView):

    def post(self, request, *args, **kwargs):
        discussion_id = request.data.get('discussion')
        
        if not discussion_id:
            return Response({'error': 'Discussion ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            discussion = Discussion.objects.get(id=discussion_id)
        except Discussion.DoesNotExist:
            return Response({'error': 'Discussion not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DiscussionEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, discussion=discussion)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
