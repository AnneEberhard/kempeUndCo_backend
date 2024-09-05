from import_export import resources
from .models import Person, Relation
from django.core.exceptions import ObjectDoesNotExist


class PersonResource(resources.ModelResource):
    """
    A resource class for importing and exporting `Person` model data using Django's import-export framework.

    This class defines how the `Person` model's data is imported and exported, including specifying the fields
    to be included and setting the import ID fields.

    Attributes:
    - model: The Django model that this resource is associated with. In this case, it is the `Person` model.
    - import_id_fields: A tuple of fields used to identify unique records during import. These fields are used
      to check if records already exist or if they should be created.
    - fields: A tuple of field names to be included in the import and export process. This includes all relevant
      attributes of the `Person` model.

    Meta class:
    - Defines the model (`Person`) that this resource operates on.
    - Specifies the fields to include in the import/export operations.
    - Defines which fields are used as unique identifiers during import operations.
    """
    class Meta:
        model = Person
        import_id_fields = ('refn', 'uid', 'name')
        fields = ('refn', 'name', 'fath_name', 'fath_refn', 'moth_name', 'moth_refn',
                  'uid', 'surn', 'givn', 'sex', 'occu', 'chan_date', 'chan_date_time',
                  'birt_date', 'birt_plac', 'deat_date', 'deat_plac', 'note',
                  'chr_date', 'chr_plac', 'buri_date', 'buri_plac', 'name_rufname',
                  'name_npfx', 'sour', 'name_nick', 'name_marnm', 'chr_addr',
                  'reli', 'marr_spou_name_1', 'marr_spou_refn_1', 'fam_husb_1',
                  'fam_wife_1', 'marr_date_1', 'marr_plac_1', 'fam_chil_1',
                  'fam_marr_1', 'fam_stat_1', 'fam_marr_1', 'marr_spou_name_2',
                  'marr_spou_refn_2', 'fam_husb_2', 'fam_wife_2', 'marr_date_2',
                  'marr_plac_2', 'fam_chil_2', 'fam_marr_2', 'fam_stat_2',
                  'fam_marr_2', 'marr_spou_name_3', 'marr_spou_refn_3',
                  'fam_husb_3', 'fam_wife_3', 'marr_date_3', 'marr_plac_3',
                  'fam_chil_3', 'fam_marr_3', 'fam_stat_3', 'fam_marr_3',
                  'marr_spou_name_4', 'marr_spou_refn_4', 'fam_husb_4',
                  'fam_wife_4', 'marr_date_4', 'marr_plac_4', 'fam_chil_4',
                  'fam_marr_4', 'fam_stat_4', 'fam_marr_4', 'obje_file_1',
                  'obje_titl_1', 'obje_file_2', 'obje_titl_2', 'obje_file_3',
                  'obje_titl_3', 'obje_file_4', 'obje_titl_4', 'obje_file_5',
                  'obje_titl_5', 'obje_file_6', 'obje_titl_6', 'confidential',
                  'family_1', 'family_2', 'creation_date', 'last_modified_date',
                  'created_by', 'last_modified_by')


class RelationResource2(resources.ModelResource):

    class Meta:
        model = Relation
        fields = ('person', 'fath_refn', 'moth_refn', 'marr_spou_refn_1',
                  'marr_date_1', 'marr_plac_1', 'children_1', 'fam_stat_1',
                  'marr_spou_refn_2', 'marr_date_2', 'marr_plac_2', 'children_2',
                  'fam_stat_2', 'marr_spou_refn_3', 'marr_date_3', 'marr_plac_3',
                  'children_3', 'fam_stat_3', 'marr_spou_refn_4', 'marr_date_4',
                  'marr_plac_4', 'children_4', 'fam_stat_4')
        import_id_fields = ('person',)  # Verwende 'person' als Import-ID

    def get_instance(self, instance_loader, row):
        try:
            person_refn = row['person']
            return self._meta.model.objects.get(person__refn=person_refn)
        except ObjectDoesNotExist:
            return None

    def before_import_row(self, row, **kwargs):
        for field_name in ['children_1', 'children_2', 'children_3', 'children_4']:
            if field_name in row:
                row[field_name] = row[field_name].split(',')

    def dehydrate_person(self, relation):
        return relation.person.refn

    def dehydrate_fath_refn(self, relation):
        return relation.fath_refn.refn if relation.fath_refn else None

    def dehydrate_moth_refn(self, relation):
        return relation.moth_refn.refn if relation.moth_refn else None

    def dehydrate_marr_spou_refn_1(self, relation):
        return relation.marr_spou_refn_1.refn if relation.marr_spou_refn_1 else None

    def dehydrate_marr_spou_refn_2(self, relation):
        return relation.marr_spou_refn_2.refn if relation.marr_spou_refn_2 else None

    def dehydrate_marr_spou_refn_3(self, relation):
        return relation.marr_spou_refn_3.refn if relation.marr_spou_refn_3 else None

    def dehydrate_marr_spou_refn_4(self, relation):
        return relation.marr_spou_refn_4.refn if relation.marr_spou_refn_4 else None

    def dehydrate_children_1(self, relation):
        return ','.join([child.refn for child in relation.children_1.all()])

    def dehydrate_children_2(self, relation):
        return ','.join([child.refn for child in relation.children_2.all()])

    def dehydrate_children_3(self, relation):
        return ','.join([child.refn for child in relation.children_3.all()])

    def dehydrate_children_4(self, relation):
        return ','.join([child.refn for child in relation.children_4.all()])

    def import_obj(self, obj, data, dry_run=False, **kwargs):
        try:
            obj.person = Person.objects.get(refn=data['person'])
        except Person.DoesNotExist:
            pass

        if data.get('fath_refn'):
            try:
                obj.fath_refn = Person.objects.get(refn=data['fath_refn'])
            except Person.DoesNotExist:
                obj.fath_refn = None

        if data.get('moth_refn'):
            try:
                obj.moth_refn = Person.objects.get(refn=data['moth_refn'])
            except Person.DoesNotExist:
                obj.moth_refn = None

        if data.get('marr_spou_refn_1'):
            try:
                obj.marr_spou_refn_1 = Person.objects.get(refn=data['marr_spou_refn_1'])
            except Person.DoesNotExist:
                obj.marr_spou_refn_1 = None

        if data.get('marr_spou_refn_2'):
            try:
                obj.marr_spou_refn_2 = Person.objects.get(refn=data['marr_spou_refn_2'])
            except Person.DoesNotExist:
                obj.marr_spou_refn_2 = None

        if data.get('marr_spou_refn_3'):
            try:
                obj.marr_spou_refn_3 = Person.objects.get(refn=data['marr_spou_refn_3'])
            except Person.DoesNotExist:
                obj.marr_spou_refn_3 = None

        if data.get('marr_spou_refn_4'):
            try:
                obj.marr_spou_refn_4 = Person.objects.get(refn=data['marr_spou_refn_4'])
            except Person.DoesNotExist:
                obj.marr_spou_refn_4 = None

        for field_name in ['children_1', 'children_2', 'children_3', 'children_4']:
            children_refns = data.get(field_name, '').split(',')
            children = []
            for refn in children_refns:
                try:
                    child = Person.objects.get(refn=refn)
                    children.append(child)
                except Person.DoesNotExist:
                    continue
            getattr(obj, field_name).set(children)

        super().import_obj(obj, data, dry_run, **kwargs)




class RelationResource(resources.ModelResource):

    class Meta:
        model = Relation
        fields = ('person', 'fath_refn', 'moth_refn', 'marr_spou_refn_1',
                  'marr_date_1', 'marr_plac_1', 'children_1', 'fam_stat_1',
                  'marr_spou_refn_2', 'marr_date_2', 'marr_plac_2', 'children_2',
                  'fam_stat_2', 'marr_spou_refn_3', 'marr_date_3', 'marr_plac_3',
                  'children_3', 'fam_stat_3', 'marr_spou_refn_4', 'marr_date_4',
                  'marr_plac_4', 'children_4', 'fam_stat_4')
        import_id_fields = ('person',)

    def before_import_row(self, row, **kwargs):
        try:
            # Mapping person using refn
            if 'person' in row:
                refn_value = row['person']
                person = Person.objects.get(refn=refn_value)
                row['person'] = person.id  # Set the correct id for ForeignKey reference

            # Processing children fields
            for field_name in ['children_1', 'children_2', 'children_3', 'children_4']:
                if field_name in row:
                    # Splitting the string of refn values and fetching corresponding Person objects
                    children_refns = row[field_name].split(',')
                    children = Person.objects.filter(refn__in=children_refns)
                    row[field_name] = ','.join([str(child.id) for child in children])  # Store ids as comma-separated string
        except ObjectDoesNotExist:
            pass  # Handle cases where a person or child is not found

    def dehydrate_person(self, relation):
        return relation.person.refn

    def dehydrate_fath_refn(self, relation):
        return relation.fath_refn.refn if relation.fath_refn else None

    def dehydrate_moth_refn(self, relation):
        return relation.moth_refn.refn if relation.moth_refn else None

    def dehydrate_marr_spou_refn_1(self, relation):
        return relation.marr_spou_refn_1.refn if relation.marr_spou_refn_1 else None

    def dehydrate_marr_spou_refn_2(self, relation):
        return relation.marr_spou_refn_2.refn if relation.marr_spou_refn_2 else None

    def dehydrate_marr_spou_refn_3(self, relation):
        return relation.marr_spou_refn_3.refn if relation.marr_spou_refn_3 else None

    def dehydrate_marr_spou_refn_4(self, relation):
        return relation.marr_spou_refn_4.refn if relation.marr_spou_refn_4 else None

    def dehydrate_children_1(self, relation):
        return ','.join([child.refn for child in relation.children_1.all()])

    def dehydrate_children_2(self, relation):
        return ','.join([child.refn for child in relation.children_2.all()])

    def dehydrate_children_3(self, relation):
        return ','.join([child.refn for child in relation.children_3.all()])

    def dehydrate_children_4(self, relation):
        return ','.join([child.refn for child in relation.children_4.all()])
