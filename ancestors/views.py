from rest_framework import generics
from .models import Person, Relation
from .serializers import PersonListSerializer, PersonSerializer, RelationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.db.models import Q

@permission_classes([IsAuthenticated])
class PersonListCreateView(generics.ListCreateAPIView):
    """
    API view to list and create Person objects.

    This view returns a list of persons filtered by the family affiliations 
    that the authenticated user is allowed to view. Only persons belonging 
    to the family trees that the user is permitted to access are displayed. 
    The user must be authenticated to access these resources.
    """
    serializer_class = PersonListSerializer

    def get_queryset(self):
        """
        Returns the queryset of persons belonging to the family trees 
        that the current user is allowed to view.

        The family trees that the user can access are determined by the groups 
        the user belongs to. The group name must start with "Stammbaum " 
        followed by the family name.
        """
        user = self.request.user
        allowed_families = set()

        # Collect all family trees the user is allowed to view
        for group in user.groups.all():
            if group.name.startswith("Stammbaum "):
                family_name = group.name.replace("Stammbaum ", "").lower()
                allowed_families.add(family_name)

        # Filter relations based on the allowed family trees and the person_id
        return Person.objects.filter(
            Q(family_1__in=allowed_families) | Q(family_2__in=allowed_families)
        ).distinct()


@permission_classes([IsAuthenticated])
class PersonDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a single Person object.

    This view allows retrieving, updating, or deleting a person based on their ID. 
    Access is restricted to persons belonging to the family trees that the 
    authenticated user is allowed to view. The user must be authenticated to 
    access these resources.
    """
    serializer_class = PersonSerializer

    def get_queryset(self):
        """
        Returns the queryset of persons belonging to the family trees 
        that the current user is allowed to view.

        The family trees that the user can access are determined by the groups 
        the user belongs to. The group name must start with "Stammbaum " 
        followed by the family name.
        """
        user = self.request.user
        allowed_families = set()

        # Collect all family trees the user is allowed to view
        for group in user.groups.all():
            if group.name.startswith("Stammbaum "):
                family_name = group.name.replace("Stammbaum ", "").lower()
                allowed_families.add(family_name)

        # Filter relations based on the allowed family trees and the person_id
        return Person.objects.filter(
            Q(family_1__in=allowed_families) | Q(family_2__in=allowed_families)
        ).distinct()


@permission_classes([IsAuthenticated])
class RelationListCreateView(generics.ListCreateAPIView):
    """
    API view to list and create Relation objects between persons.

    This view returns a list of relations between persons, filtered by the 
    family affiliations that the authenticated user is allowed to view. 
    The user must be authenticated to access these resources.
    """
    serializer_class = RelationSerializer

    def get_queryset(self):
        """
        Returns the queryset of relations involving persons belonging to the family 
        trees that the current user is allowed to view.

        The family trees that the user can access are determined by the groups 
        the user belongs to. The group name must start with "Stammbaum " 
        followed by the family name.
        """
        user = self.request.user
        allowed_families = set()

        # Collect all family trees the user is allowed to view
        for group in user.groups.all():
            if group.name.startswith("Stammbaum "):
                family_name = group.name.replace("Stammbaum ", "").lower()
                allowed_families.add(family_name)

        # Filter relations based on the allowed family trees and the person_id
        return Relation.objects.filter(
            Q(person__family_1__in=allowed_families) | Q(person__family_2__in=allowed_families)
        ).distinct()


@permission_classes([IsAuthenticated])
class RelationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a single Relation object.

    This view allows retrieving, updating, or deleting a relation between 
    two persons based on the person_id. Access is restricted to relations 
    involving persons belonging to the family trees that the authenticated 
    user is allowed to view. The user must be authenticated to access these resources.
    """
    serializer_class = RelationSerializer
    lookup_field = 'person_id'

    def get_queryset(self):
        """
        Returns the queryset of relations involving persons belonging to the family 
        trees that the current user is allowed to view.

        The family trees that the user can access are determined by the groups 
        the user belongs to. The group name must start with "Stammbaum " 
        followed by the family name. The queryset is filtered by the `person_id` 
        to find the specific relation.
        """
        user = self.request.user
        allowed_families = set()

        # Collect all family trees the user is allowed to view
        for group in user.groups.all():
            if group.name.startswith("Stammbaum "):
                family_name = group.name.replace("Stammbaum ", "").lower()
                allowed_families.add(family_name)

        # Filter relations based on the allowed family trees and the person_id
        return Relation.objects.filter(
            Q(person__family_1__in=allowed_families) | Q(person__family_2__in=allowed_families),
            person_id=self.kwargs['person_id']
        ).distinct()
