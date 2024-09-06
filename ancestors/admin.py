from accounts import models
from .resources import PersonResource, RelationResource
from .models import Person, Relation
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.contrib.admin import SimpleListFilter


class PersonAdmin(ImportExportModelAdmin):
    resource_class = PersonResource
    list_display = ('id', 'name', 'note', 'family_1', 'family_2', 'birt_date', 'deat_date', 'confidential')  # Felder, die in der Listenansicht angezeigt werden
    list_filter = ('family_1', 'family_2')
    search_fields = ('name', 'id')  # Felder, die durchsuchbar sind
    readonly_fields = ('name', 'refn', 'creation_date', 'last_modified_date', 'created_by', 'last_modified_by')

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
        ('Name und Notizen', {
            'fields': ('name_rufname', 'name_npfx', 'note', 'sour', 'name_nick', 'name_marnm')
        }),
        ('Bilddateien', {
            'fields': ('obje_file_1', 'obje_titl_1', 'obje_file_2', 'obje_titl_2', 'obje_file_3', 'obje_titl_3',
                       'obje_file_4', 'obje_titl_4', 'obje_file_5', 'obje_titl_5', 'obje_file_6', 'obje_titl_6'),
            'classes': ('collapse',),
        }),
        ('Vertraulichkeit', {
            'fields': ('confidential', 'family_1', 'family_2')
        }),
        ('Metadaten', {
            'fields': ('creation_date', 'last_modified_date', 'created_by', 'last_modified_by'),
            'classes': ('collapse',),  # Optional: macht diesen Abschnitt einklappbar
        }),
        ('Familiendaten', {
            'fields': ('fath_refn', 'moth_refn', 'marr_spou_name_1', 'marr_spou_refn_1', 'fam_husb_1',
                'fam_wife_1', 'marr_date_1', 'marr_plac_1', 'fam_chil_1',
                'fam_marr_1', 'fam_stat_1',
                'marr_spou_name_2', 'marr_spou_refn_2', 'fam_husb_2', 'fam_wife_2', 'marr_date_2',
                'marr_plac_2', 'fam_chil_2', 'fam_marr_2', 'fam_stat_2',
                'marr_spou_name_3', 'marr_spou_refn_3', 'fam_husb_3', 'fam_wife_3', 'marr_date_3',
                'marr_plac_3', 'fam_chil_3', 'fam_marr_3', 'fam_stat_3',
                'marr_spou_name_4', 'marr_spou_refn_4', 'fam_husb_4', 'fam_wife_4', 'marr_date_4',
                'marr_plac_4', 'fam_chil_4', 'fam_marr_4', 'fam_stat_4',),
            'classes': ('collapse',)
        })
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        allowed_families = request.user.allowed_families
        return qs.filter(family_1__in=allowed_families) | qs.filter(family_2__in=allowed_families)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def save_model(self, request, obj, form, change):
        obj.save(user=request.user)


class Family1Filter(SimpleListFilter):
    title = 'Family 1'
    parameter_name = 'person__family_1'

    def lookups(self, request, model_admin):
        families = set(Person.objects.values_list('family_1', flat=True).distinct())
        return [(family, family) for family in families if family]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(person__family_1=self.value())
        return queryset


class Family2Filter(SimpleListFilter):
    title = 'Family 2'
    parameter_name = 'person__family_2'

    def lookups(self, request, model_admin):
        families = set(Person.objects.values_list('family_2', flat=True).distinct())
        return [(family, family) for family in families if family]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(person__family_2=self.value())
        return queryset


class RelationAdmin(ImportExportModelAdmin):
    resource_class = RelationResource
    list_display = ('person', 'fath_refn', 'moth_refn',
                    'marr_spou_refn_1', 'display_children_1',
                    'marr_spou_refn_2', 'display_children_2',
                    'marr_spou_refn_3', 'display_children_3',
                    'marr_spou_refn_4', 'display_children_4')
    search_fields = ('person__name', 'fath_refn__name', 'moth_refn__name', 'marr_spou_refn_1__name', 'marr_spou_refn_2__name', 'marr_spou_refn_3__name', 'marr_spou_refn_4__name')
    raw_id_fields = ('fath_refn', 'moth_refn', 'marr_spou_refn_1', 'marr_spou_refn_2', 'marr_spou_refn_3', 'marr_spou_refn_4')
    filter_horizontal = ('children_1', 'children_2', 'children_3', 'children_4')
    list_filter = (Family1Filter, Family2Filter)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        allowed_families = request.user.allowed_families
        return qs.filter(
            person__family_1__in=allowed_families
        ) | qs.filter(
            person__family_2__in=allowed_families
        )

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

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


admin.site.register(Person, PersonAdmin)
admin.site.register(Relation, RelationAdmin)
