from rest_framework import serializers
from .models import Person, Relation


class PersonSerializer(serializers.ModelSerializer):
    """
    Serializer for the Person model that includes all relevant fields for detailed
    representation of a person.

    Fields:
    - id: The unique identifier of the person.
    - refn: Reference number for the person.
    - name: The full name of the person.
    - surn: Surname of the person.
    - givn: Given name of the person.
    - sex: Gender of the person.
    - occu: Occupation of the person.
    - chan_date: Date when the record was last changed.
    - chan_date_time: Date and time when the record was last changed.
    - birt_date: Birth date of the person.
    - birth_date_formatted: Formatted birth date of the person.
    - birt_plac: Place of birth.
    - deat_date: Date of death.
    - death_date_formatted: Formatted date of death.
    - deat_plac: Place of death.
    - note: Additional notes about the person.
    - chr_date: Date of christening.
    - chr_plac: Place of christening.
    - buri_date: Date of burial.
    - buri_plac: Place of burial.
    - name_rufname: Rufname (nickname) of the person.
    - name_npfx: Name prefix (e.g., Dr., Mr.).
    - sour: Source of the information.
    - name_nick: Nickname of the person.
    - name_marnm: Name after marriage.
    - chr_addr: Address at the time of christening.
    - reli: Religion of the person.
    - obje_file_1: File field 1 associated with the person.
    - obje_file_2: File field 2 associated with the person.
    - obje_file_3: File field 3 associated with the person.
    - obje_file_4: File field 4 associated with the person.
    - obje_file_5: File field 5 associated with the person.
    - obje_file_6: File field 6 associated with the person.
    - confidential: Confidentiality status of the person's information.
    """
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
        ref_name = 'AncestorsPersonSerializer'

    def to_representation(self, instance):
        """
        Customize the representation of the Person instance based on its confidentiality status.

        Parameters:
        - instance: The Person instance to be serialized.

        Returns:
        - A dictionary representing the serialized data of the Person instance with customized fields based on confidentiality:
            - If the `confidential` field is 'yes', most fields will be masked (set to empty strings), except for the `id` and `confidential` fields.
            - If the `confidential` field is 'restricted', only the `name` field will be included with its value; all other fields will be masked (set to empty strings).
           - If the `confidential` field is neither 'yes' nor 'restricted', the standard representation is returned.
        """
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
    """
    Serializer for the Person model that customizes the representation
    of the `Person` instances based on their confidentiality status.

    Fields:
    - id: The unique identifier of the person.
    - name: The name of the person.
    - surn: The surname of the person.
    - givn: The given name of the person.
    """
    class Meta:
        model = Person
        fields = [
            'id',
            'name',
            'surn',
            'givn'
        ]

    def to_representation(self, instance):
        """
        Customize the representation of the Person instance based on
        the confidentiality status.

        If the `confidential` field is 'yes', the name is masked as 'vertraulich',
        and surname and given name are omitted.

        If the `confidential` field is 'restricted', the name is included, but
        the surname and given name are omitted.

        Parameters:
        - instance: The Person instance to be serialized.

        Returns:
        - A dictionary representing the serialized data of the Person instance.
        """
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
    """
    Serializer for the Relation model that includes all fields of the Relation instance.

    Fields:
    - All fields of the Relation model.
    """
    class Meta:
        model = Relation
        fields = '__all__'
