from django.db.models import Q
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import views
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ancestors.models import Person
from .models import Discussion, DiscussionEntry
from .serializers import DiscussionEntrySerializer, DiscussionSerializer


class DiscussionListView(generics.ListAPIView):
    serializer_class = DiscussionSerializer
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
        """Filtert die Diskussionen basierend auf den erlaubten Stammbaum-Namen des Benutzers."""
        allowed_family_trees = self.get_allowed_family_trees()
        if not allowed_family_trees:
            return Discussion.objects.none()  # Keine Diskussionen zurückgeben, wenn keine erlaubten Stammbäume vorhanden sind

        return Discussion.objects.filter(
            Q(person__family_tree_1__in=allowed_family_trees) |
            Q(person__family_tree_2__in=allowed_family_trees)
        ).distinct()


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


@permission_classes([IsAuthenticated])
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


@permission_classes([IsAuthenticated])
class DiscussionEntryDetailView(APIView):
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


# not yet tested:
class DiscussionDetailCreateView(views.APIView):
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