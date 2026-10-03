from django.db import transaction
from rest_framework import generics
from .models import Person, Relation
from .serializers import AdminPersonSerializer, AdminRelationSerializer, PersonListSerializer, PersonSerializer, RelationSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.decorators import permission_classes
from django.db.models import Q
from utils.change_log import log_person_changes, log_relation_changes, get_relation_field_value
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from rest_framework.response import Response


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
            'surn',
            'givn',
            'sex',
            'occu',
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
            'obje_file_1',
            'obje_file_2',
            'obje_file_3',
            'obje_file_4',
            'obje_file_5',
            'obje_file_6',
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
    permission_classes = [IsTreeAdmin]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Relation.objects.all()

        allowed_families = user.allowed_families

        return (
            Relation.objects.filter(
                Q(person__family_1__in=allowed_families)
                | Q(person__family_2__in=allowed_families)
            )
            .distinct()
        )

    def get_object(self):
        refn = self.kwargs['refn']

        "No Relation matches the given query."

        relation = get_object_or_404(
        self.get_queryset(),
        person__refn=refn,
    )

        return relation

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        refn = self.kwargs['refn']

        relation_tracked_fields = [
            'fath_refn',
            'moth_refn',

            'marr_spou_refn_1',
            'marr_date_1',
            'marr_plac_1',
            'fam_stat_1',
            'children_1',

            'marr_spou_refn_2',
            'marr_date_2',
            'marr_plac_2',
            'fam_stat_2',
            'children_2',

            'marr_spou_refn_3',
            'marr_date_3',
            'marr_plac_3',
            'fam_stat_3',
            'children_3',

            'marr_spou_refn_4',
            'marr_date_4',
            'marr_plac_4',
            'fam_stat_4',
            'children_4',
        ]

        relation = self.get_queryset().filter(
            person__refn=refn
        ).first()

        if relation is None:
            person = get_object_or_404(
                Person,
                refn=refn,
            )

            relation = Relation.objects.create(
                person=person
            )

        old_values = {
            field_name: get_relation_field_value(relation, field_name)
            for field_name in relation_tracked_fields
        }

        serializer = self.get_serializer(
            relation,
            data=request.data,
            partial=True,
        )

        print(
    'RELATION VOR UPDATE:',
    relation.pk,
    relation.person_id,
    relation.person.refn,
)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        print(
    'RELATION NACH UPDATE:',
    relation.pk,
    relation.person_id,
    relation.person.refn,
)
        new_values = {
            field_name: get_relation_field_value(relation, field_name)
            for field_name in relation_tracked_fields
            }

        log_relation_changes(
            relation=relation,
            old_values=old_values, new_values=new_values,
            requested_fields=serializer.validated_data,
            user=self.request.user,
        )

        return Response(serializer.data)


class AdminPersonCreateView(generics.CreateAPIView):
    serializer_class = AdminPersonSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        person = serializer.save(user=request.user)

        relation = Relation.objects.create(
            person=person
        )

        return Response(
            {
                'person': AdminPersonSerializer(person).data,
                'relation': AdminRelationSerializer(relation).data,
            },
            status=status.HTTP_201_CREATED
        )
    