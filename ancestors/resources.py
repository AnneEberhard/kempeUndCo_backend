from import_export import resources
from .models import Person, Relation


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


class RelationResource(resources.ModelResource):
    """
    A resource class for importing and exporting `Relation` model data using Django's import-export framework.

    This class handles the conversion and processing of `Relation` model data for import and export operations,
    including the parsing of Many-to-Many relationships.

    Attributes:
    - model: The Django model that this resource is associated with. In this case, it is the `Relation` model.
    - import_id_fields: A tuple of fields used to uniquely identify records during import. This field is used to
      check if records should be updated or created.

    Meta class:
    - Defines the model (`Relation`) that this resource operates on.
    - Specifies the fields to be included in the import/export operations.
    - Defines which fields are used as unique identifiers during import operations.

    Methods:
    - before_import_row(row, **kwargs): Converts the IDs in Many-to-Many fields into lists of IDs before importing
      the row. This ensures that the imported data is correctly formatted for processing.
    """
    class Meta:
        model = Relation
        import_id_fields = ('person',)  # Use 'person' as the import ID
        fields = ('person', 'fath_refn', 'moth_refn', 'marr_spou_refn_1',
                  'marr_date_1', 'marr_plac_1', 'children_1', 'fam_stat_1',
                  'marr_spou_refn_2', 'marr_date_2', 'marr_plac_2', 'children_2',
                  'fam_stat_2', 'marr_spou_refn_3', 'marr_date_3', 'marr_plac_3',
                  'children_3', 'fam_stat_3', 'marr_spou_refn_4', 'marr_date_4',
                  'marr_plac_4', 'children_4', 'fam_stat_4')

    def before_import_row(self, row, **kwargs):
        """
        Converts the IDs in Many-to-Many fields into lists of IDs before importing the row.

        This method ensures that any comma-separated values in Many-to-Many fields are split into lists, which
        allows the import process to handle the relationships correctly.

        Parameters:
        - row: The row of data being imported.
        - **kwargs: Additional keyword arguments.

        Returns:
        - None: The row is modified in place.
        """
        for field_name in ['children_1', 'children_2', 'children_3', 'children_4']:
            if field_name in row:
                row[field_name] = row[field_name].split(',')
