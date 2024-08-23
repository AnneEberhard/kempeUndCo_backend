from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from infos.models import Info

class InfoAdmin(ImportExportModelAdmin):
    model = Info
    list_display = ('id', 'title', 'author')
    

admin.site.register(Info, InfoAdmin)
