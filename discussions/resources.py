from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, Widget
from django.contrib.auth import get_user_model
from import_export.instance_loaders import BaseInstanceLoader

from .models import Discussion, Person, DiscussionEntry

User = get_user_model()

class DiscussionResource(resources.ModelResource):

    person = fields.Field(
        column_name='person',
        attribute='person',
        widget=ForeignKeyWidget(Person, 'refn')
    )

    class Meta:
        model = Discussion


class DiscussionWidget(Widget):

    def clean(self, value, row=None, **kwargs):
        return Discussion.objects.get(
            person__refn=value
        )

    def render(self, value, obj=None, **kwargs):
        if value:
            return value.person.refn
        return ""


class DiscussionEntryResource(resources.ModelResource):

    discussion = fields.Field(
        column_name="discussion_refn",
        attribute="discussion",
        widget=DiscussionWidget()
    )

    author = fields.Field(
        column_name="author_email",
        attribute="author",
        widget=ForeignKeyWidget(User, "email")
    )

    class Meta:
        model = DiscussionEntry
        force_init_instance = True
    
    def get_import_id_fields(self):
        print("IMPORT IDS:", super().get_import_id_fields())
        return super().get_import_id_fields()
