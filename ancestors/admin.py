from import_export import resources
from import_export.fields import Field
from import_export.widgets import DateWidget
from .models import Person
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

class PersonResource(resources.ModelResource):
    class Meta:
        model = Person
        import_id_fields = ('refn', 'uid', 'name')  # Hier werden nur die relevanten Felder angegeben
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
                  'obje_titl_5', 'obje_file_6', 'obje_titl_6', 'confidential')


class PersonAdmin(ImportExportModelAdmin):
    resource_class = PersonResource
    list_display = ('id', 'name', 'refn', 'note', 'birt_date', 'deat_date', 'confidential')  # Felder, die in der Listenansicht angezeigt werden
    search_fields = ('refn', 'uid', 'name')  # Felder, die durchsuchbar sind


admin.site.register(Person, PersonAdmin)