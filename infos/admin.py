from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from infos.models import Info


class InfoAdmin(ImportExportModelAdmin):
    model = Info
    list_display = ('id', 'title', 'author')
   # exclude = ('image_1_thumbnail', 'image_2_thumbnail', 'image_3_thumbnail', 'image_4_thumbnail')

admin.site.register(Info, InfoAdmin)
