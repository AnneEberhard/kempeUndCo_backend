from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from comments.models import Comment
from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from infos.models import Info
from recipes.models import Recipe


class InfoFamilyFilter(SimpleListFilter):
    """
    A Django admin filter for filtering `Info` objects by their associated `family_1` or `family_2` fields.

    The filter displays distinct family values from the `Info` model, allowing admin users
    to filter the queryset based on the selected family.
    """
    title = 'Info Family'
    parameter_name = 'info__family_1'

    def lookups(self, request, model_admin):
        families = set(Info.objects.values_list('family_1', flat=True).distinct())
        return [(family, family) for family in families if family]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(info__family_1=self.value()) | queryset.filter(info__family_2=self.value())
        return queryset


class RecipeFamilyFilter(SimpleListFilter):
    """
    A Django admin filter for filtering `Recipe` objects by their associated `family_1` or `family_2` fields.

    The filter displays distinct family values from the `Recipe` model, allowing admin users
    to filter the queryset based on the selected family.
    """
    title = 'Recipe Family'
    parameter_name = 'recipe__family_1'

    def lookups(self, request, model_admin):
        families = set(Recipe.objects.values_list('family_1', flat=True).distinct())
        return [(family, family) for family in families if family]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(recipe__family_1=self.value()) | queryset.filter(recipe__family_2=self.value())
        return queryset


class CommentsAdmin(ImportExportModelAdmin):
    """
    Custom Django admin configuration for the `Comment` model.

    Displays comments with additional filters for `Info` and `Recipe` families.
    Filters the queryset based on the logged-in user's allowed families unless the user is a superuser.
    """
    model = Comment
    list_display = ('id', 'author', 'info', 'recipe', 'famInfo')
    list_filter = (InfoFamilyFilter, RecipeFamilyFilter)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        allowed_families = request.user.allowed_families
        return qs.filter(
            (Q(info__family_1__in=allowed_families) | Q(info__family_2__in=allowed_families)) |
            (Q(recipe__family_1__in=allowed_families) | Q(recipe__family_2__in=allowed_families))
        )


admin.site.register(Comment, CommentsAdmin)
