from rest_framework import generics
from .models import Person, Relation
from .serializers import PersonListSerializer, PersonSerializer, RelationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


@permission_classes([IsAuthenticated])
class PersonListCreateView(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonListSerializer


@permission_classes([IsAuthenticated])
class PersonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


@permission_classes([IsAuthenticated])
class RelationListCreateView(generics.ListCreateAPIView):
    queryset = Relation.objects.all()
    serializer_class = RelationSerializer

@permission_classes([IsAuthenticated])
class RelationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Relation.objects.all()
    serializer_class = RelationSerializer
    lookup_field = 'person_id'

    def get_queryset(self):
        return Relation.objects.filter(person_id=self.kwargs['person_id'])
