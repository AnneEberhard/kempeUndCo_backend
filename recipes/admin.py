from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from recipes.models import Recipe


class RecipeAdmin(ImportExportModelAdmin):
    model = Recipe
    list_display = ('id', 'title', 'author')


admin.site.register(Recipe, RecipeAdmin)
