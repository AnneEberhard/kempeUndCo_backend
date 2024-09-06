from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'username', 'email', 'get_allowed_families', )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('guarantor', 'guarantor_email', 'family_1', 'family_2', 'notes')}),
    )

    def get_allowed_families(self, obj):
        return ', '.join(obj.allowed_families)
    get_allowed_families.short_description = 'Allowed Families'


    def get_queryset(self, request):
        # Beschränke den Queryset auf Benutzer, die nicht superuser sind
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_superuser=False)

    def get_form(self, request, obj=None, **kwargs):
        # Verhindere, dass staff-Benutzer Berechtigungen ändern können
        form = super().get_form(request, obj, **kwargs)
        is_superuser = getattr(obj, 'is_superuser', False)

        if not request.user.is_superuser:
            if 'is_superuser' in form.base_fields:
                form.base_fields['is_superuser'].disabled = True
            if 'user_permissions' in form.base_fields:
                form.base_fields['user_permissions'].disabled = True
            if 'groups' in form.base_fields:
                form.base_fields['groups'].disabled = True

        return form


admin.site.register(CustomUser, CustomUserAdmin)
