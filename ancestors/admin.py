from accounts import models
from .resources import PersonResource, RelationResource
from .models import Person, PersonChangeLog, Relation
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .services import add_child_to_relationship, add_spouse, remove_child_from_relationship, remove_parent_from_child, remove_spouse, sync_child_from_parent, sync_person_legacy_fields, sync_spouse_data



class PersonAdmin(ImportExportModelAdmin):
    """
    Admin configuration for the `Person` model.

    This class customizes the admin interface by:
    - Displaying specific fields in the list and filter views.
    - Providing search functionality for `name` and `id`.
    - Making certain fields read-only.
    - Organizing fields into collapsible sections for better organization.
    - Filtering the queryset based on the user's allowed families, unless the user is a superuser.
    - Restricting delete permissions to superusers only.
    - Customizing the save behavior to include the current user.

    **Fieldsets:**
    - `None`: Basic person information.
    - `Geburts- und Sterbedaten`: Birth and death details.
    - `Taufe und Beerdigung`: Baptism and burial details.
    - `Name und Notizen`: Names and notes.
    - `Bilddateien`: Image files, collapsible.
    - `Vertraulichkeit`: Confidentiality settings.
    - `Metadaten`: Metadata, collapsible.
    - `Familiendaten`: Family data, collapsible.
    """
    resource_class = PersonResource
    list_display = ('id', 'name', 'note', 'family_1', 'family_2', 'birt_date', 'deat_date', 'confidential')  # Felder, die in der Listenansicht angezeigt werden
    list_filter = ('family_1', 'family_2')
    search_fields = ('name', 'id', 'refn')
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
    """
    Custom filter for the `RelationAdmin` to filter relations by `family_1` of the related person.
    """
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
    """
    Custom filter for the `RelationAdmin` to filter relations by `family_2` of the related person.
    """
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
    """
    Admin configuration for the `Relation` model.

    This class customizes the admin interface by:
    - Displaying specific fields in the list view.
    - Providing search functionality across related persons and their relations.
    - Using `raw_id_fields` for foreign key relations to improve performance.
    - Enabling horizontal filtering for the `children` fields.
    - Adding custom filters for `family_1` and `family_2` of the related person.
    - Restricting queryset based on the user's allowed families unless the user is a superuser.
    - Displaying children names in a comma-separated list for each marriage.
    - Restricting delete permissions to superusers only.
    """
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

    def save_model(self, request, obj, form, change):
        old_father = None
        old_mother = None
        old_spouses = {}

        if change:
            old_obj = Relation.objects.get(pk=obj.pk)
            old_father = old_obj.fath_refn
            old_mother = old_obj.moth_refn
            old_spouses = {
                index: getattr(old_obj, f"marr_spou_refn_{index}")
                for index in range(1, 5)
            }

        super().save_model(request, obj, form, change)

        new_father = obj.fath_refn
        new_mother = obj.moth_refn
        new_spouses = {
            index: getattr(obj, f"marr_spou_refn_{index}")
            for index in range(1, 5)
        }

        if old_father != new_father:

            if old_father:
                remove_child_from_relationship(
                    parent=old_father,
                    other_parent=old_mother,
                    child=obj.person,
                )

                if old_mother:
                    remove_child_from_relationship(
                        parent=old_mother,
                        other_parent=old_father,
                        child=obj.person,
                    )

            if new_father:
                add_child_to_relationship(
                    parent=new_father,
                    other_parent=new_mother,
                    child=obj.person,
                )

                if new_mother:
                    add_child_to_relationship(
                        parent=new_mother,
                        other_parent=new_father,
                        child=obj.person,
                    )

        if old_mother != new_mother:

            if old_mother:
                remove_child_from_relationship(
                    parent=old_mother,
                    other_parent=old_father,
                    child=obj.person,
                )

                if old_father:
                    remove_child_from_relationship(
                        parent=old_father,
                        other_parent=old_mother,
                        child=obj.person,
                    )

            if new_mother:
                add_child_to_relationship(
                    parent=new_mother,
                    other_parent=new_father,
                    child=obj.person,
                )

                if new_father:
                    add_child_to_relationship(
                        parent=new_father,
                        other_parent=new_mother,
                        child=obj.person,
                    )

        for index in range(1, 5):
            old_spouse = old_spouses.get(index)
            new_spouse = new_spouses[index]

            if old_spouse and old_spouse != new_spouse:
                remove_spouse(
                    person=old_spouse,
                    spouse=obj.person,
                )

                sync_person_legacy_fields(old_spouse)

            if new_spouse:
                sync_spouse_data(
                    person=obj.person,
                    spouse=new_spouse,
                    marr_date=getattr(
                        obj,
                        f"marr_date_{index}"
                    ),
                    marr_plac=getattr(
                        obj,
                        f"marr_plac_{index}"
                    ),
                    fam_stat=getattr(
                        obj,
                        f"fam_stat_{index}"
                    ),
                )

            if new_spouse and old_spouse != new_spouse:
                add_spouse(
                    person=new_spouse,
                    spouse=obj.person,
                    preferred_slot=index,
                )

                sync_person_legacy_fields(new_spouse)

        sync_person_legacy_fields(obj.person)

        if old_father:
            sync_person_legacy_fields(old_father)

        if new_father:
            sync_person_legacy_fields(new_father)

        if old_mother:
            sync_person_legacy_fields(old_mother)

        if new_mother:
            sync_person_legacy_fields(new_mother)

    def save_form(self, request, form, change):
        if change:
            old_obj = Relation.objects.get(pk=form.instance.pk)

            form._old_children = {
                index: set(
                    getattr(old_obj, f"children_{index}")
                    .values_list("pk", flat=True)
                )
                for index in range(1, 5)
            }
        else:
            form._old_children = {
                index: set()
                for index in range(1, 5)
            }

        return super().save_form(request, form, change)

    def save_related(self, request, form, formsets, change):
        old_children = form._old_children

        super().save_related(request, form, formsets, change)

        obj = form.instance

        new_children = {
            index: set(
                getattr(obj, f"children_{index}")
                .values_list("pk", flat=True)
            )
            for index in range(1, 5)
        }

        for index in range(1, 5):
            removed_children = (
                old_children[index] - new_children[index]
            )
            added_children = (
                new_children[index] - old_children[index]
            )

            for child_pk in removed_children:
                child = Person.objects.get(pk=child_pk)
    
                remove_parent_from_child(
                    parent=obj.person,
                    child=child,
                )
    
                sync_person_legacy_fields(child)
    
            for child_pk in added_children:
                child = Person.objects.get(pk=child_pk)
    
                sync_child_from_parent(
                    parent=obj.person,
                    child=child,
                )

                sync_person_legacy_fields(child)

        sync_person_legacy_fields(obj.person)


class PersonChangeLogAdmin(ImportExportModelAdmin):
    list_display = (
        'person',
        'changed_at',
        'changed_by',
        'field_name',
        'old_value',
        'new_value',
        'change_id'
    )

    list_filter = (
        'changed_by',
        'field_name',
        'changed_at',
    )

    search_fields = (
        'person__refn',
        'person__name',
        'field_name',
        'old_value',
        'new_value',
    )

    readonly_fields = (
        'person',
        'changed_by',
        'changed_at',
        'field_name',
        'old_value',
        'new_value',
    )

admin.site.register(Person, PersonAdmin)
admin.site.register(Relation, RelationAdmin)
admin.site.register(PersonChangeLog, PersonChangeLogAdmin)
