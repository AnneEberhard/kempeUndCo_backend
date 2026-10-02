from rest_framework import serializers
from .models import Person, Relation
from .services import add_child_to_relationship, add_spouse, remove_child_from_relationship, remove_parent_from_child, remove_spouse, sync_child_from_parent, sync_person_legacy_fields, sync_spouse_data


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
                'refn': instance.refn,
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
                'refn': instance.refn,
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
            'givn',
            'refn'
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
                'givn': '',
                'refn': ''
            }
        elif instance.confidential == 'restricted':
            return {
                'id': instance.id,
                'name': instance.name,
                'surn': '',
                'givn': '',
                'refn': instance.refn
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


class AdminPersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = [
            'id',
            'refn',
            'name',

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

            'marr_spou_name_1',
            'marr_spou_refn_1',
            'fam_husb_1',
            'fam_wife_1',
            'marr_date_1',
            'marr_plac_1',
            'fam_chil_1',
            'fam_marr_1',
            'fam_stat_1',

            'marr_spou_name_2',
            'marr_spou_refn_2',
            'fam_husb_2',
            'fam_wife_2',
            'marr_date_2',
            'marr_plac_2',
            'fam_chil_2',
            'fam_marr_2',
            'fam_stat_2',

            'marr_spou_name_3',
            'marr_spou_refn_3',
            'fam_husb_3',
            'fam_wife_3',
            'marr_date_3',
            'marr_plac_3',
            'fam_chil_3',
            'fam_marr_3',
            'fam_stat_3',

            'marr_spou_name_4',
            'marr_spou_refn_4',
            'fam_husb_4',
            'fam_wife_4',
            'marr_date_4',
            'marr_plac_4',
            'fam_chil_4',
            'fam_marr_4',
            'fam_stat_4',

            'obje_file_1',
            'obje_titl_1',
            'obje_file_2',
            'obje_titl_2',
            'obje_file_3',
            'obje_titl_3',
            'obje_file_4',
            'obje_titl_4',
            'obje_file_5',
            'obje_titl_5',
            'obje_file_6',
            'obje_titl_6',

            'confidential',
            'family_1',
            'family_2',

            'creation_date',
            'last_modified_date',
            'created_by',
            'last_modified_by',
        ]

        read_only_fields = [
            'id',
            'refn',
            'name',
            'birth_date_formatted',
            'death_date_formatted',

            'creation_date',
            'last_modified_date',
            'created_by',
            'last_modified_by',
        ]

    def create(self, validated_data):
        user = validated_data.pop('user', None)

        person = Person(**validated_data)
        person.save(user=user)

        return person


class AdminRelationSerializer(serializers.ModelSerializer):
    fath_refn = serializers.SlugRelatedField(
        slug_field='refn',
        queryset=Person.objects.all(),
        allow_null=True,
        required=False,
    )
    moth_refn = serializers.SlugRelatedField(
        slug_field='refn',
        queryset=Person.objects.all(),
        allow_null=True,
        required=False,
    )

    fath_name = serializers.CharField(
        source='fath_refn.name',
        read_only=True,
        allow_null=True,
    )
    moth_name = serializers.CharField(
        source='moth_refn.name',
        read_only=True,
        allow_null=True,
    )
    marr_spou_refn_1 = serializers.SlugRelatedField(
        slug_field='refn',
        queryset=Person.objects.all(),
        allow_null=True,
        required=False,
    )

    marr_spou_refn_2 = serializers.SlugRelatedField(
        slug_field='refn',
        queryset=Person.objects.all(),
        allow_null=True,
        required=False,
    )

    marr_spou_refn_3 = serializers.SlugRelatedField(
        slug_field='refn',
        queryset=Person.objects.all(),
        allow_null=True,
        required=False,
    )

    marr_spou_refn_4 = serializers.SlugRelatedField(
        slug_field='refn',
        queryset=Person.objects.all(),
        allow_null=True,
        required=False,
    )

    children_1 = serializers.SlugRelatedField(
        slug_field='refn',
        queryset=Person.objects.all(),
        many=True,
        required=False,
    )

    children_2 = serializers.SlugRelatedField(
        slug_field='refn',
        queryset=Person.objects.all(),
        many=True,
        required=False,
    )

    children_3 = serializers.SlugRelatedField(
        slug_field='refn',
        queryset=Person.objects.all(),
        many=True,
        required=False,
    )

    children_4 = serializers.SlugRelatedField(
        slug_field='refn',
        queryset=Person.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Relation
        fields = [
            'fath_refn',
            'fath_name',
            'moth_refn',
            'moth_name',

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

    def update(self, instance, validated_data):
    
        old_father = instance.fath_refn
        old_mother = instance.moth_refn
        old_spouses = {
            index: getattr(
                instance,
                f"marr_spou_refn_{index}"
            )
            for index in range(1, 5)
        }

        old_children = {
            index: set(
                getattr(
                    instance,
                    f"children_{index}"
                ).values_list("pk", flat=True)
            )
            for index in range(1, 5)
        }
    
        instance = super().update(
            instance,
            validated_data
        )
    
        new_father = instance.fath_refn
        new_mother = instance.moth_refn
        new_spouses = {
            index: getattr(
                instance,
                f"marr_spou_refn_{index}"
            )
            for index in range(1, 5)
        }
        new_children = {
            index: set(
                getattr(
                    instance,
                    f"children_{index}"
                ).values_list("pk", flat=True)
            )
            for index in range(1, 5)
        }
    
        if old_father and old_father != new_father:
            remove_child_from_relationship(
                parent=old_father,
                other_parent=new_mother,
                child=instance.person,
            )

            if old_mother:
                remove_child_from_relationship(
                    parent=old_mother,
                    other_parent=old_father,
                    child=instance.person,
                )
    
        if new_father and old_father != new_father:
            add_child_to_relationship(
                parent=new_father,
                other_parent=new_mother,
                child=instance.person,
            )

            if new_mother:
                add_child_to_relationship(
                    parent=new_mother,
                    other_parent=new_father,
                    child=instance.person,
                )

        if old_mother and old_mother != new_mother:
            remove_child_from_relationship(
                parent=old_mother,
                other_parent=new_father,
                child=instance.person,
            )

        if new_mother and old_mother != new_mother:
            add_child_to_relationship(
                parent=new_mother,
                other_parent=new_father,
                child=instance.person,
            )

        for index in range(1, 5):

            removed_children = (
                old_children[index] - new_children[index]
            )

            added_children = (
                new_children[index] - old_children[index]
            )

            # Kinder wurden aus children_X entfernt
            for child_pk in removed_children:
                removed_child = Person.objects.get(
                    pk=child_pk
                )
                print("removed_child: ", removed_child.refn)
                remove_parent_from_child(parent=instance.person, child=removed_child)

            # Kinder wurden direkt in children_X eingetragen
            for child_pk in added_children:
                added_child = Person.objects.get(
                    pk=child_pk
                )
                print("added_child: ", added_child.refn)

                sync_child_from_parent(
                    parent=instance.person,
                    child=added_child,
                )
            
        for index in range(1, 5):
            old_spouse = old_spouses[index]
            new_spouse = new_spouses[index]

            # Alten Ehepartner beim anderen entfernen
            if old_spouse and old_spouse != new_spouse:
                remove_spouse(
                    person=old_spouse,
                    spouse=instance.person,
                )

            # Neuen Ehepartner beim anderen eintragen
            if new_spouse:
                sync_spouse_data(
                                    person=instance.person,
                                    spouse=new_spouse,
                                    marr_date=getattr(
                                        instance,
                                        f"marr_date_{index}"
                                    ),
                                    marr_plac=getattr(
                                        instance,
                                        f"marr_plac_{index}"
                                    ),
                                    fam_stat=getattr(
                                        instance,
                                        f"fam_stat_{index}"
                                    ),
                                )
                if old_spouse != new_spouse:
                    add_spouse(
                        person=new_spouse,
                        spouse=instance.person,
                        preferred_slot=index,
                    )
                    sync_person_legacy_fields(old_spouse)
                    sync_person_legacy_fields(new_spouse)

                    print("old spouse: ", old_spouse)
                    print("new spouse: ", new_spouse)
                
        sync_person_legacy_fields(instance.person)
        if old_father:
            sync_person_legacy_fields(old_father)

        if new_father:
            sync_person_legacy_fields(new_father)

        if old_mother:
            sync_person_legacy_fields(old_mother)

        if new_mother:
            sync_person_legacy_fields(new_mother)

        return instance
