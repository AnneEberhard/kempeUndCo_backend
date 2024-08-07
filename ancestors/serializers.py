from rest_framework import serializers
from .models import Person, Relation

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'  # oder liste spezifische Felder auf, z.B. ['id', 'name', 'refn', ...]


class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = '__all__'  # oder liste spezifische Felder auf, z.B. ['id', 'person', 'fath_refn', ...]
