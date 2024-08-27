from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from comments.models import Comment

class CommentsAdmin(ImportExportModelAdmin):
    model = Comment
    list_display = ('id', 'author', 'info', 'recipe')
    

admin.site.register(Comment, CommentsAdmin)
