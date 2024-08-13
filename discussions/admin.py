from django.contrib import admin
from .models import Discussion, DiscussionEntry


class DiscussionEntryInline(admin.TabularInline):
    model = DiscussionEntry
    extra = 1


class DiscussionPageAdmin(admin.ModelAdmin):
    inlines = [DiscussionEntryInline]


admin.site.register(Discussion, DiscussionPageAdmin)
admin.site.register(DiscussionEntry)
