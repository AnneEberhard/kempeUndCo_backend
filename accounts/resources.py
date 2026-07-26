from accounts.models import CustomUser
from import_export import resources

class CustomUserResource(resources.ModelResource):

    class Meta:
        model = CustomUser
        import_id_fields = ('email',)
        fields = ('username', 'email','author_name',  'family_1', 'family_2', 'guarantor', 'guarantor_email', 'notes')
        export_order = ('id', 'username', 'email', 'author_name', 'family_1', 'family_2', 'guarantor', 'guarantor_email', 'notes')
