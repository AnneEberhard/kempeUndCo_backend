from datetime import datetime
from import_export import resources
from import_export.fields import Field
from import_export.widgets import DateWidget
from .models import Person, RelatedData
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
                  'obje_titl_5', 'obje_file_6', 'obje_titl_6', 'confidential', 'family_tree_1', 'family_tree_2')


class PersonAdmin(ImportExportModelAdmin):
    resource_class = PersonResource
    list_display = ('id', 'name', 'refn', 'note', 'birt_date', 'deat_date', 'confidential')  # Felder, die in der Listenansicht angezeigt werden
    search_fields = ('refn', 'name')  # Felder, die durchsuchbar sind
    exclude = ('fath_name', 'fath_refn', 'moth_name', 'moth_refn',
                'uid', 'marr_spou_name_1', 'marr_spou_refn_1', 'fam_husb_1',
                'fam_wife_1', 'marr_date_1', 'marr_plac_1', 'fam_chil_1',
                'fam_marr_1', 'fam_stat_1',
                'marr_spou_name_2', 'marr_spou_refn_2', 'fam_husb_2', 'fam_wife_2', 'marr_date_2',
                'marr_plac_2', 'fam_chil_2', 'fam_marr_2', 'fam_stat_2',
                'marr_spou_name_3', 'marr_spou_refn_3', 'fam_husb_3', 'fam_wife_3', 'marr_date_3',
                'marr_plac_3', 'fam_chil_3', 'fam_marr_3', 'fam_stat_3',
                'marr_spou_name_4', 'marr_spou_refn_4', 'fam_husb_4', 'fam_wife_4', 'marr_date_4',
                'marr_plac_4', 'fam_chil_4', 'fam_marr_4', 'fam_stat_4' )

    def save_model(self, request, obj, form, change):
        # Wenn das Modell neu erstellt wird oder bearbeitet wird
        if not change:
            # Wenn es sich um eine neue Instanz handelt, aber der Name bereits gesetzt ist
            if obj.birt_date:
                try:
                    birth_date = datetime.strptime(obj.birt_date, '%d.%m.%Y').date()
                    obj.birth_date_formatted = birth_date
                except ValueError:
                    obj.birth_date_formatted = None
            if obj.deat_date:
                try:
                    death_date = datetime.strptime(obj.deat_date, '%d.%m.%Y').date()
                    obj.death_date_formatted = death_date
                except ValueError:
                    obj.death_date_formatted = None
        else:
            # Wenn das Modell bearbeitet wird
            if obj.birt_date and not obj.birth_date_formatted:
                try:
                    birth_date = datetime.strptime(obj.birt_date, '%d.%m.%Y').date()
                    obj.birth_date_formatted = birth_date
                except ValueError:
                    obj.birth_date_formatted = None
            if obj.deat_date and not obj.death_date_formatted:
                try:
                    death_date = datetime.strptime(obj.deat_date, '%d.%m.%Y').date()
                    obj.death_date_formatted = death_date
                except ValueError:
                    obj.death_date_formatted = None

        super().save_model(request, obj, form, change)

class RelatedDataAdmin(admin.ModelAdmin):
    list_display = ('person', 'fath_refn', 'moth_refn', 'marr_spou_refn_1', 'marr_spou_refn_2', 'marr_spou_refn_3', 'marr_spou_refn_4', 'display_children_1', 'display_children_2', 'display_children_3', 'display_children_4')
    search_fields = ('person__name', 'fath_refn__name', 'moth_refn__name', 'marr_spou_refn_1__name', 'marr_spou_refn_2__name', 'marr_spou_refn_3__name', 'marr_spou_refn_4__name')
    raw_id_fields = ('fath_refn', 'moth_refn', 'marr_spou_refn_1', 'marr_spou_refn_2', 'marr_spou_refn_3', 'marr_spou_refn_4')
    filter_horizontal = ('children_1', 'children_2', 'children_3', 'children_4')

    def display_children_1(self, obj):
        return ", ".join([child.name for child in obj.children_1.all()])
    display_children_1.short_description = 'Kinder aus Ehe 1'

    def display_children_2(self, obj):
        return ", ".join([child.name for child in obj.children_2.all()])
    display_children_2.short_description = 'Kinder aus Ehe 2'

    def display_children_3(self, obj):
        return ", ".join([child.name for child in obj.children_3.all()])
    display_children_3.short_description = 'Kinder aus Ehe 3'

    def display_children_4(self, obj):
        return ", ".join([child.name for child in obj.children_4.all()])
    display_children_4.short_description = 'Kinder aus Ehe 4'


admin.site.register(Person, PersonAdmin)
admin.site.register(RelatedData, RelatedDataAdmin)