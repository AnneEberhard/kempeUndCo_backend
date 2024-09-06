from django.db.models import Q
from rest_framework import generics, status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ancestors.models import Person
from .models import Discussion, DiscussionEntry
from .serializers import DiscussionSerializer, DiscussionEntrySerializer


class DiscussionListView(generics.ListAPIView):
    """
    API view to list discussions based on the allowed family trees for the current user.

    Methods:
    - get_allowed_families: Returns the set of allowed family names for the current user.
    - get_queryset: Filters and returns the queryset of discussions the user is allowed to see.
    """
    serializer_class = DiscussionSerializer
    permission_classes = [IsAuthenticated]

    def get_allowed_families(self):
        """Retrieves the allowed family tree names for the current user."""
        user = self.request.user
        allowed_families = set()

        if user.family_1:
            allowed_families.add(user.family_1.lower())
        if user.family_2:
            allowed_families.add(user.family_2.lower())

        return allowed_families

    def get_queryset(self):
        """Filters discussions based on the allowed family tree names of the user."""
        allowed_families = self.get_allowed_families()
        if not allowed_families:
            return Discussion.objects.none()  # Return no discussions if no allowed families are found

        return Discussion.objects.filter(
            Q(person__family_1__in=allowed_families) | Q(person__family_2__in=allowed_families)
        ).distinct()


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_or_create_discussion(request, id):
    """
    API view to retrieve or create a discussion for a specific person.

    This view handles GET requests to retrieve an existing discussion and POST
    requests to create a new discussion if one does not already exist for the
    person with the provided ID.

    Parameters:
    - id: The ID of the person linked to the discussion.

    Returns:
    - On success: The discussion data and a 200 or 201 status code.
    - On failure: An error message and a 404 status code if the person or discussion is not found.
    """
    try:
        person = Person.objects.get(id=id)
    except Person.DoesNotExist:
        return Response({'error': 'Person not found'}, status=404)

    discussion, created = Discussion.objects.get_or_create(person=person)
    serializer = DiscussionSerializer(discussion, context={'request': request})

    return Response(serializer.data, status=201 if created else 200)


@permission_classes([IsAuthenticated])
class CreateDiscussionEntryView(views.APIView):
    """
    API view to create a new discussion entry in an existing discussion.

    This view handles POST requests to add a new entry to a discussion.
    The user must provide the discussion ID and the entry data.

    Methods:
    - post: Validates the request data, creates a new discussion entry,
      and associates it with the discussion and the author.
    """
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


@permission_classes([IsAuthenticated])
class DiscussionEntryDetailView(views.APIView):
    """
    API view to retrieve, update, or delete a specific discussion entry.

    This view handles GET, PUT, and DELETE requests for a discussion entry
    identified by its primary key (pk). The user must be the author to update
    or delete the entry.

    Methods:
    - get_object: Retrieves the discussion entry object or returns None if not found.
    - get: Returns the discussion entry data.
    - put: Updates the discussion entry if the request user is the author.
    - delete: Deletes the discussion entry if the request user is the author.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return DiscussionEntry.objects.get(pk=pk)
        except DiscussionEntry.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        entry = self.get_object(pk)
        if entry:
            serializer = DiscussionEntrySerializer(entry)
            return Response(serializer.data)
        return Response({'error': 'Discussion entry not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, *args, **kwargs):
        entry = self.get_object(pk)
        if entry:
            if entry.author != request.user:
                return Response({'error': 'You are not the author of this entry'}, status=status.HTTP_403_FORBIDDEN)
            serializer = DiscussionEntrySerializer(entry, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Discussion entry not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, *args, **kwargs):
        entry = self.get_object(pk)
        if entry:
            if entry.author != request.user:
                return Response({'error': 'You are not the author of this entry'}, status=status.HTTP_403_FORBIDDEN)
            entry.delete()
            return Response({'message': 'Discussion entry deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Discussion entry not found'}, status=status.HTTP_404_NOT_FOUND)


class DiscussionDetailCreateView(views.APIView):
    """
    API view to retrieve or create a discussion for a specific person.

    This view handles GET requests to retrieve a discussion for a given person ID
    and POST requests to create a new discussion if one does not already exist.

    Methods:
    - get_person: Helper method to retrieve the Person object by ID.
    - get: Returns the discussion data or an error if not found.
    - post: Creates a new discussion for the person or returns the existing discussion.
    """
    permission_classes = [IsAuthenticated]

    def get_person(self, id):
        """Helper method to get a person by ID."""
        try:
            return Person.objects.get(id=id)
        except Person.DoesNotExist:
            return None

    def get(self, request, id):
        person = self.get_person(id)
        if person is None:
            return Response({'error': 'Person not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            discussion = Discussion.objects.get(person=person)
            serializer = DiscussionSerializer(discussion)
            return Response(serializer.data)
        except Discussion.DoesNotExist:
            return Response({'error': 'Discussion not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, id):
        person = self.get_person(id)
        if person is None:
            return Response({'error': 'Person not found'}, status=status.HTTP_404_NOT_FOUND)

        discussion, created = Discussion.objects.get_or_create(person=person)
        serializer = DiscussionSerializer(discussion)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
