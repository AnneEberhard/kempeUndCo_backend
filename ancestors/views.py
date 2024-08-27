from rest_framework import generics
from .models import Person, Relation
from .serializers import PersonListSerializer, PersonSerializer, RelationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.db.models import Q

@permission_classes([IsAuthenticated])
class PersonListCreateView(generics.ListCreateAPIView):
    serializer_class = PersonListSerializer

    def get_queryset(self):
        user = self.request.user
        allowed_trees = set()

        # Sammle alle Stammbäume, die der Benutzer sehen darf
        for group in user.groups.all():
            if group.name.startswith("Stammbaum "):
                tree_name = group.name.replace("Stammbaum ", "").lower()
                allowed_trees.add(tree_name)

        # Filtere Personen basierend auf den erlaubten Stammbäumen
        return Person.objects.filter(
            Q(family_tree_1__in=allowed_trees) | Q(family_tree_2__in=allowed_trees)
        ).distinct()


@permission_classes([IsAuthenticated])
class PersonDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PersonSerializer

    def get_queryset(self):
        user = self.request.user
        allowed_trees = set()

        # Sammle alle Stammbäume, die der Benutzer sehen darf
        for group in user.groups.all():
            if group.name.startswith("Stammbaum "):
                tree_name = group.name.replace("Stammbaum ", "").lower()
                allowed_trees.add(tree_name)

        # Filtere Personen basierend auf den erlaubten Stammbäumen
        return Person.objects.filter(
            Q(family_tree_1__in=allowed_trees) | Q(family_tree_2__in=allowed_trees)
        ).distinct()


@permission_classes([IsAuthenticated])
class RelationListCreateView(generics.ListCreateAPIView):
    serializer_class = RelationSerializer

    def get_queryset(self):
        user = self.request.user
        allowed_trees = set()

        # Sammle alle Stammbäume, die der Benutzer sehen darf
        for group in user.groups.all():
            if group.name.startswith("Stammbaum "):
                tree_name = group.name.replace("Stammbaum ", "").lower()
                allowed_trees.add(tree_name)

        # Filtere Beziehungen basierend auf den erlaubten Stammbäumen
        return Relation.objects.filter(
            Q(person__family_tree_1__in=allowed_trees) | Q(person__family_tree_2__in=allowed_trees)
        ).distinct()


@permission_classes([IsAuthenticated])
class RelationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RelationSerializer
    lookup_field = 'person_id'

    def get_queryset(self):
        user = self.request.user
        allowed_trees = set()

        # Sammle alle Stammbäume, die der Benutzer sehen darf
        for group in user.groups.all():
            if group.name.startswith("Stammbaum "):
                tree_name = group.name.replace("Stammbaum ", "").lower()
                allowed_trees.add(tree_name)

        # Filtere Beziehungen basierend auf den erlaubten Stammbäumen und der person_id
        return Relation.objects.filter(
            Q(person__family_tree_1__in=allowed_trees) | Q(person__family_tree_2__in=allowed_trees),
            person_id=self.kwargs['person_id']
        ).distinct()
