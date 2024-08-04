from .resources import PersonResource, RelationResource
from .models import Person, Relation
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin


class PersonAdmin(ImportExportModelAdmin):
    resource_class = PersonResource
    list_display = ('id', 'name', 'refn', 'note', 'birt_date', 'deat_date', 'confidential')  # Felder, die in der Listenansicht angezeigt werden
    search_fields = ('refn', 'name')  # Felder, die durchsuchbar sind
    readonly_fields = ('creation_date', 'last_modified_date', 'created_by', 'last_modified_by')

    fieldsets = (
        (None, {
            'fields': ('refn', 'name', 'surn', 'givn', 'sex', 'occu')
        }),
        ('Geburts- und Sterbedaten', {
            'fields': ('birt_date', 'birth_date_formatted', 'birt_plac', 'deat_date', 'death_date_formatted', 'deat_plac')
        }),
        ('Taufe und Beerdigung', {
            'fields': ('chr_date', 'chr_plac', 'chr_addr', 'reli', 'buri_date', 'buri_plac')
        }),
        ('Name und Quellen', {
            'fields': ('name_rufname', 'name_npfx', 'sour', 'name_nick', 'name_marnm')
        }),
        ('Bilddateien', {
            'fields': ('obje_file_1', 'obje_titl_1', 'obje_file_2', 'obje_titl_2', 'obje_file_3', 'obje_titl_3', 
                       'obje_file_4', 'obje_titl_4', 'obje_file_5', 'obje_titl_5', 'obje_file_6', 'obje_titl_6'),
            'classes': ('collapse',),
        }),
        ('Vertraulichkeit', {
            'fields': ('confidential', 'family_tree_1', 'family_tree_2')
        }),
        ('Metadaten', {
            'fields': ('creation_date', 'last_modified_date', 'created_by', 'last_modified_by'),
            'classes': ('collapse',),  # Optional: macht diesen Abschnitt einklappbar
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.save(user=request.user)

class RelationAdmin(ImportExportModelAdmin):
    resource_class = RelationResource
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
admin.site.register(Relation, RelationAdmin)