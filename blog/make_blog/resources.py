from import_export import resources
from .models import Blog

class BlogAdminResource(resources.ModelResource):

    class Meta:
        model   =   Blog
        import_id_fields = ('blog_id',)
        exclude = ('id',)