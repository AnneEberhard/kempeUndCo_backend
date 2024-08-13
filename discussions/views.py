# discussions/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ancestors.models import Person
from .models import Discussion
from .serializers import DiscussionSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_or_create_discussion(request, refn):
    try:
        person = Person.objects.get(refn=refn)
    except Person.DoesNotExist:
        return Response({'error': 'Person not found'}, status=404)

    discussion, created = Discussion.objects.get_or_create(person=person)
    serializer = DiscussionSerializer(discussion)

    return Response(serializer.data, status=201 if created else 200)
