from django.contrib import admin
from .models import Discussion, DiscussionEntry


class DiscussionEntryInline(admin.TabularInline):
    model = DiscussionEntry
    extra = 1


class DiscussionPageAdmin(admin.ModelAdmin):
    inlines = [DiscussionEntryInline]

    list_display = ('id', 'discussion_for', 'created_at', 'updated_at')

    def discussion_for(self, obj):
        return f"{obj.person.id} - {obj.person.name}"

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class DiscussionEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'discussion_for', 'author', 'created_at', 'updated_at')

    def discussion_for(self, obj):
        return f"{obj.discussion.person.id} - {obj.discussion.person.name}"


admin.site.register(Discussion, DiscussionPageAdmin)
admin.site.register(DiscussionEntry, DiscussionEntryAdmin)
