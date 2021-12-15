from django.contrib import admin
from django.http.request import HttpRequest
from .models import Comment, ContactClass,BlogCategory,Blog,UserModel,Images, not_verified_user
from .utils import urlify

# Register your models here.
admin.site.site_header = "Cool Developer Admin Panel"
admin.site.site_title = " Cool Developer Admin Portal"
admin.site.index_title = "Welcome to Cool Developer Admin Portal"

@admin.action(description='Draft Content')
def make_draft(modeladmin, request: HttpRequest, queryset):
    queryset.update(blog_status='d')

@admin.action(description='Mark selected content as published')
def make_published(modeladmin, request: HttpRequest, queryset):
    queryset.update(blog_status='p')  

@admin.action(description='Withdraw Content')
def withdrawContent(modeladmin, request: HttpRequest, queryset):
    queryset.update(blog_status='w')

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
    list_filter = ["blog_status"]
    actions = [make_published, make_draft, withdrawContent]
    def get_queryset(self, request: HttpRequest):
        qs = super(BlogAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(blog_author=request.user)
    def save_model(self, request: HttpRequest, obj: Blog, form, change):
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
        # css = ["css/blog_style.css"]
        js = ["js/tinymce.js"]
        css = {
        'all': ("css/blog_style.css",)
         }

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'timestamp']
    search_fields = ['id', 'user', 'timestamp', 'parent']
    def has_change_permission(self, request: HttpRequest, obj = ...) -> bool:
        return False
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    def has_delete_permission(self, request: HttpRequest, obj = ...) -> bool:
        return True

@admin.register(ContactClass)
class ContactModel(admin.ModelAdmin):
    list_display = ["query_id","customer_email","query_subject","query_resolved","date"]
    list_display_links = ["query_id","customer_email"]
    list_filter = ['query_resolved']
    search_fields = ["query_id","customer_email","customer_name","query_subject","date","query_resolved"]
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

@admin.register(Images)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['image_id', 'image','timestamp']
    search_fields = ['image_id', 'image','timestamp']

@admin.register(UserModel)
class UserModelClass(admin.ModelAdmin):
    list_display = ['user','avatar_image']

@admin.register(not_verified_user)
class NotVerifiedUserClass(admin.ModelAdmin):
    list_display = ['id','username','email','date_joined']
    list_display_links = ['id', 'username']
    list_display = ['id','username','email','date_joined']
    search_fields = ['id','username','email','date_joined', 'first_name', 'last_name']
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    def has_change_permission(self, request: HttpRequest, obj= ...) -> bool:
        return False
    def has_delete_permission(self, request: HttpRequest, obj = ...) -> bool:
        return request.user.is_superuser
