from import_export import resources
from .models import Blog, Configuration

class BlogAdminResource(resources.ModelResource):

    class Meta:
        model   =   Blog
        import_id_fields = ('blog_id',)
        exclude = ('id',)

class SettingAdminResource(resources.ModelResource):
    class Meta:
        model = Configuration