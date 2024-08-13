from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'username', 'email')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('guarantor', 'guarantor_email','family_1', 'family_2', 'notes')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
