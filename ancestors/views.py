from django.db import transaction
from rest_framework import generics
from .models import Person, Relation
from .serializers import AdminPersonSerializer, AdminRelationSerializer, PersonListSerializer, PersonSerializer, RelationSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.decorators import permission_classes
from django.db.models import Q
from utils.change_log import log_person_changes
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


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
        """
        user = self.request.user
        allowed_families = set()

        if user.family_1:
            allowed_families.add(user.family_1.lower())
        if user.family_2:
            allowed_families.add(user.family_2.lower())

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
        """
        user = self.request.user
        allowed_families = set()

        if user.family_1:
            allowed_families.add(user.family_1.lower())
        if user.family_2:
            allowed_families.add(user.family_2.lower())

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
        """
        user = self.request.user
        allowed_families = set()

        if user.family_1:
            allowed_families.add(user.family_1.lower())
        if user.family_2:
            allowed_families.add(user.family_2.lower())

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
        """
        user = self.request.user
        allowed_families = set()

        if user.family_1:
            allowed_families.add(user.family_1.lower())
        if user.family_2:
            allowed_families.add(user.family_2.lower())

        return Relation.objects.filter(
            Q(person__family_1__in=allowed_families) | Q(person__family_2__in=allowed_families),
            person_id=self.kwargs['person_id']
        ).distinct()


class IsTreeAdmin(BasePermission):
    """
    Zugriff auf den Stammbaum-Editor nur für Staff- und Superuser.
    Die konkrete Familienberechtigung wird über das QuerySet geregelt.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_active
            and (
                request.user.is_staff
                or request.user.is_superuser
            )
        )



class AdminPersonDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = AdminPersonSerializer
    lookup_field = 'refn'
    permission_classes = [IsTreeAdmin]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Person.objects.all()

        allowed_families = user.allowed_families

        return (
            Person.objects.filter(family_1__in=allowed_families)
            | Person.objects.filter(family_2__in=allowed_families)
        ).distinct()

    @transaction.atomic
    def perform_update(self, serializer):
        person = self.get_object()

        tracked_fields = [
            'fath_name',
            'fath_refn',
            'moth_name',
            'moth_refn',
            'uid',
            'surn',
            'givn',
            'sex',
            'occu',
            'chan_date',
            'chan_date_time',
            'birt_date',
            'birt_plac',
            'deat_date',
            'deat_plac',
            'note',
            'chr_date',
            'chr_plac',
            'buri_date',
            'buri_plac',
            'name_rufname',
            'name_npfx',
            'sour',
            'name_nick',
            'name_marnm',
            'chr_addr',
            'reli',
            'confidential',
            'family_1',
            'family_2',
        ]

        old_values = {
            field: getattr(person, field)
            for field in tracked_fields
        }

        serializer.save(user=self.request.user)
        person = serializer.instance

        for index in range(1, 7):
            delete_field = f'delete_obje_file_{index}'

            if self.request.data.get(delete_field) == 'true':
                image_field = f'obje_file_{index}'
                setattr(person, image_field, None)

        for i in range(1, 7):
            field = getattr(person, f'obje_file_{i}')
            print(
                'VOR SAVE:',
                i,
                field.name if field and field.name else None
            )
        person.save(user=self.request.user)
        for i in range(1, 7):
            field = getattr(person, f'obje_file_{i}')
            print(
                'NACH SAVE:',
                i,
                field.name if field and field.name else None
            )
        log_person_changes(
            person=person,
            old_values=old_values, new_values=serializer.validated_data,
            user=self.request.user,
        )


class AdminPersonListView(generics.ListAPIView):
    serializer_class = AdminPersonSerializer
    permission_classes = [IsTreeAdmin]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = Person.objects.all()
        else:
            allowed_families = user.allowed_families

            queryset = (
                Person.objects.filter(family_1__in=allowed_families)
                | Person.objects.filter(family_2__in=allowed_families)
            ).distinct()

        search = self.request.query_params.get('search', '').strip()

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(refn__icontains=search)
            )

        return queryset.order_by('name')


class AdminRelationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = AdminRelationSerializer
    #permission_classes = [IsTreeAdmin]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Relation.objects.all()

        #allowed_families = user.allowed_families
        allowed_families = ['kempe', 'huenten']

        return (
            Relation.objects.filter(
                Q(person__family_1__in=allowed_families)
                | Q(person__family_2__in=allowed_families)
            )
            .distinct()
        )

    def get_object(self):
        refn = self.kwargs['refn']

        return get_object_or_404(
            self.get_queryset(),
            person__refn=refn,
        )

    @transaction.atomic
    def perform_update(self, serializer):
        relation = self.get_object()

        old_father = relation.fath_refn
        old_mother = relation.moth_refn

        new_father = serializer.validated_data.get(
            'fath_refn',
            old_father,
        )
        new_mother = serializer.validated_data.get(
            'moth_refn',
            old_mother,
        )

        child = relation.person

        # Alte Vaterbeziehung entfernen
        if old_father != new_father:
            self._remove_child_from_parent(
                child=child,
                parent=old_father
            )

        # Alte Mutterbeziehung entfernen
        if old_mother != new_mother:
            self._remove_child_from_parent(
                child=child,
                parent=old_mother
            )

        # Jetzt den neuen Zustand speichern.
        # Die bestehenden Signals kümmern sich um das Hinzufügen
        # der neuen Beziehungen.
        serializer.save()

    def _remove_child_from_parent(self, child, parent):
        if not parent:
            return

        parent_relation = Relation.objects.filter(
            person=parent
        ).first()

        if not parent_relation:
            return

        for i in range(1, 5):
            children_field = getattr(
                parent_relation,
                f'children_{i}',
            )

            if children_field.filter(pk=child.pk).exists():
                parent_relation._updating = True

                try:
                    children_field.remove(child)
                    parent_relation.save()
                finally:
                    parent_relation._updating = False

                break
