from import_export import resources
from import_export.fields import Field
from import_export.widgets import DateWidget
from .models import Person

class PersonResource(resources.ModelResource):
    class Meta:
        model = Person
        import_id_fields = ('refn',)
        fields = ('refn', 'uid', 'name', 'surname', 'birth_date')


# Admin-Integration
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

@admin.register(Person)
class PersonAdmin(ImportExportModelAdmin):
    resource_class = PersonResource
