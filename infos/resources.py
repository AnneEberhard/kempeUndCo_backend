from django.contrib.auth import get_user_model
from import_export import fields
from import_export.widgets import ForeignKeyWidget

from import_resources import TimestampRestoreResource
from .models import Info

User = get_user_model()


class InfoResource(TimestampRestoreResource):

    author = fields.Field(
        column_name="author_email",
        attribute="author",
        widget=ForeignKeyWidget(User, "email")
    )

    class Meta:
        model = Info