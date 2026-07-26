from accounts.models import CustomUser
from import_export import resources

class CustomUserResource(resources.ModelResource):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email','authorname',  'family_1', 'family_2', 'guarantor', 'guarantor_email', 'notes')
        export_order = ('id', 'username', 'email', 'authorname', 'family_1', 'family_2', 'guarantor', 'guarantor_email', 'notes')
