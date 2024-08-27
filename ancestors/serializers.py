from rest_framework import serializers
from .models import Person, Relation


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            'id',
            'refn',
            'name',
            'surn',
            'givn',
            'sex',
            'occu',
            'chan_date',
            'chan_date_time',
            'birt_date',
            'birth_date_formatted',
            'birt_plac',
            'deat_date',
            'death_date_formatted',
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
            'obje_file_1',
            'obje_file_2',
            'obje_file_3',
            'obje_file_4',
            'obje_file_5',
            'obje_file_6',
            'confidential'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.confidential == 'yes':
            return {
                'id': instance.id,
                'name': 'vertraulich',
                'surn': '',
                'givn': '',
                'sex': '',
                'occu': '',
                'chan_date': '',
                'chan_date_time': '',
                'birt_date': '',
                'birth_date_formatted': '',
                'birt_plac': '',
                'deat_date': '',
                'death_date_formatted': '',
                'deat_plac': '',
                'note': '',
                'chr_date': '',
                'chr_plac': '',
                'buri_date': '',
                'buri_plac': '',
                'name_rufname': '',
                'name_npfx': '',
                'sour': '',
                'name_nick': '',
                'name_marnm': '',
                'chr_addr': '',
                'reli': '',
                'obje_file_1': '',
                'obje_file_2': '',
                'obje_file_3': '',
                'obje_file_4': '',
                'obje_file_5': '',
                'obje_file_6': '',
                'confidential': instance.confidential
            }
        elif instance.confidential == 'restricted':
            return {
                'id': instance.id,
                'name': instance.name,
                'surn': '',
                'givn': '',
                'sex': '',
                'occu': '',
                'chan_date': '',
                'chan_date_time': '',
                'birt_date': '',
                'birth_date_formatted': '',
                'birt_plac': '',
                'deat_date': '',
                'death_date_formatted': '',
                'deat_plac': '',
                'note': '',
                'chr_date': '',
                'chr_plac': '',
                'buri_date': '',
                'buri_plac': '',
                'name_rufname': '',
                'name_npfx': '',
                'sour': '',
                'name_nick': '',
                'name_marnm': '',
                'chr_addr': '',
                'reli': '',
                'obje_file_1': '',
                'obje_file_2': '',
                'obje_file_3': '',
                'obje_file_4': '',
                'obje_file_5': '',
                'obje_file_6': '',
                'confidential': instance.confidential
            }
        return representation


class PersonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            'id',
            'name',
            'surn',
            'givn'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.confidential == 'yes':
            return {
                'id': instance.id,
                'name': 'vertraulich',
                'surn': '',
                'givn': ''
            }
        elif instance.confidential == 'restricted':
            return {
                'id': instance.id,
                'name': instance.name,
                'surn': '',
                'givn': ''
            }
        return representation


class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = '__all__'
