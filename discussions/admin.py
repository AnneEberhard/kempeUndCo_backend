from django.contrib import admin

from ancestors.models import Person
from .models import Discussion, DiscussionEntry
from django.db.models import Q
from django.contrib.admin import SimpleListFilter
from import_export.admin import ImportExportModelAdmin


class PersonFamilyFilter(SimpleListFilter):
    title = 'Person Family'
    parameter_name = 'person__family_1'

    def lookups(self, request, model_admin):
        families = set(Person.objects.values_list('family_1', flat=True).distinct())
        return [(family, family) for family in families if family]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(person__family_1=self.value()) | queryset.filter(person__family_2=self.value())
        return queryset


class DiscussionEntryInline(admin.TabularInline):
    model = DiscussionEntry
    extra = 1


class DiscussionPageAdmin(ImportExportModelAdmin):
    inlines = [DiscussionEntryInline]

    list_display = ('id', 'discussion_for', 'created_at', 'updated_at')
    list_filter = (PersonFamilyFilter,)

    def discussion_for(self, obj):
        return f"{obj.person.id} - {obj.person.name}"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        allowed_families = request.user.allowed_families
        return qs.filter(
            Q(person__family_1__in=allowed_families) | Q(person__family_2__in=allowed_families)
        )

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class DiscussionEntryAdmin(ImportExportModelAdmin):
    list_display = ('id', 'discussion_for', 'author', 'created_at', 'updated_at')

    def discussion_for(self, obj):
        return f"{obj.discussion.person.id} - {obj.discussion.person.name}"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        allowed_families = request.user.allowed_families
        return qs.filter(
            Q(discussion__person__family_1__in=allowed_families) | Q(discussion__person__family_2__in=allowed_families)
        )


admin.site.register(Discussion, DiscussionPageAdmin)
admin.site.register(DiscussionEntry, DiscussionEntryAdmin)
