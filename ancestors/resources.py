from import_export import resources
from .models import Person, Relation


class PersonResource(resources.ModelResource):
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
    class Meta:
        model = Relation
        import_id_fields = ('person',)  # Verwenden Sie 'person' als Import-ID
        fields = ('person', 'fath_refn', 'moth_refn', 'marr_spou_refn_1',
                  'marr_date_1', 'marr_plac_1', 'children_1', 'fam_stat_1',
                  'marr_spou_refn_2', 'marr_date_2', 'marr_plac_2', 'children_2',
                  'fam_stat_2', 'marr_spou_refn_3', 'marr_date_3', 'marr_plac_3',
                  'children_3', 'fam_stat_3', 'marr_spou_refn_4', 'marr_date_4',
                  'marr_plac_4', 'children_4', 'fam_stat_4')

    def before_import_row(self, row, **kwargs):
        # Konvertieren Sie die IDs der Many-to-Many-Felder in eine Liste von IDs
        for field_name in ['children_1', 'children_2', 'children_3', 'children_4']:
            if field_name in row:
                row[field_name] = row[field_name].split(',')
