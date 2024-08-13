from rest_framework import generics
from .models import Person, Relation
from .serializers import PersonSerializer, RelationSerializer


class PersonListCreateView(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class PersonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class RelationListCreateView(generics.ListCreateAPIView):
    queryset = Relation.objects.all()
    serializer_class = RelationSerializer


class RelationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Relation.objects.all()
    serializer_class = RelationSerializer
    lookup_field = 'person_id'  # Verwende person_id als Lookup-Feld

    def get_queryset(self):
        return Relation.objects.filter(person_id=self.kwargs['person_id'])
