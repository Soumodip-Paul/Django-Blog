from django.contrib import admin
from .models import ContactClass,BlogCategory,Blog,UserModel
from .utils import urlify

# Register your models here.
admin.site.site_header = "Cool Developer Admin Panel"
admin.site.site_title = " Cool Developer Admin Portal"
admin.site.index_title = "Welcome to Cool Developer Admin Portal"

@admin.action(description='Mark selected content as published')
def make_published(modeladmin, request, queryset):
    queryset.update(blog_status='p')  

@admin.action(description='Draft Content')
def make_draft(modeladmin, request, queryset):
    queryset.update(blog_status='d')

@admin.action(description='Withdraw Content')
def withdrawContent(modeladmin, request, queryset):
    queryset.update(blog_status='w')

@admin.register(UserModel)
class UserModelClass(admin.ModelAdmin):
    list_display = ['user','avatar_image']

@admin.register(ContactClass)
class ContactModel(admin.ModelAdmin):
    list_display = ["query_id","customer_email","customer_name","query_subject","date"]
    list_display_links = ["query_id","customer_email"]
    search_fields = ["query_id","customer_email","customer_name","query_subject","date"]

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ["id","category_name","category_url","date"]
    list_display_links = ["id",]
    search_fields = ["id","category_name","category_url","date"]
    list_editable = ["category_name","category_url",]

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["blog_id","blog_title", "blog_status","blog_category","blog_date"]
    list_display_links = ["blog_id","blog_title",]
    search_fields = ["blog_id","blog_title", "blog_status","blog_category","blog_date"]
    list_editable = ["blog_status","blog_category"]
    actions = [make_published, make_draft, withdrawContent]
    def get_queryset(self, request):
        qs = super(BlogAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(blog_author=request.user)
    def save_model(self, request, obj, form, change):
        # associating the current logged in user to the client_id
        obj.blog_author = request.user
        if obj.blog_url == '':
            obj.blog_url = urlify(obj.blog_title)
            isAvailable = Blog.objects.filter(blog_url=obj.blog_url)
            print(isAvailable)
            if len(isAvailable) != 0 :
                obj.blog_url = obj.blog_url + "-" + str(Blog.objects.count() + 1)
        super().save_model(request, obj, form, change)
    class Media: 
        js = ["js/tinymce.js"]