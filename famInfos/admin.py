from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from famInfos.models import FamInfo


class FamInfoAdmin(ImportExportModelAdmin):
    """
    Admin configuration for the `famInfo` model.

    This class customizes the admin interface by:
    - Displaying specific fields (`id`, `title`, `author`) in the list view.
    - Adding filters for `family_1` and `family_2` fields to easily filter `famInfo` entries by family.
    - Excluding the `image_*_thumbnail` fields from the admin form, as these are likely auto-generated and not meant to be edited manually.
    - Restricting the queryset based on the user's allowed families unless the user is a superuser.
    """
    model = FamInfo
    list_display = ('id', 'title', 'author')
    list_filter = ('family_1', 'family_2')
    exclude = ('image_1_thumbnail', 'image_2_thumbnail', 'image_3_thumbnail', 'image_4_thumbnail')

    def get_queryset(self, request):
        """
        Override the default queryset to filter based on the allowed families for the current user,
        unless the user is a superuser.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        allowed_families = request.user.allowed_families
        return qs.filter(family_1__in=allowed_families) | qs.filter(family_2__in=allowed_families)


admin.site.register(FamInfo, FamInfoAdmin)
