from pickle import TRUE
from django.contrib import admin
from django.db import OperationalError
from django.http.request import HttpRequest
from import_export.admin import ImportExportMixin
from .models import *
from .resources import BlogAdminResource, SettingAdminResource
from .utils import getPlayListdata, getYoutubeVideoData, urlify
try: 
    setting : Configuration = Configuration.load()
    site_name = setting.site_name
except Configuration.DoesNotExist as e:
    site_name = "Cool Developer"
except OperationalError as e:
    site_name = "Cool Developer"

def registerPanel(site_name) :
    admin.site.site_header = "{name} Admin Panel".format(name=site_name )
    admin.site.site_title = " {name} Admin Portal".format(name=site_name )
    admin.site.index_title = "Welcome to {name} Admin Portal".format( name=site_name )

@admin.action(description='Draft Content')
def make_draft(modeladmin, request: HttpRequest, queryset):
    queryset.update(blog_status='d')

@admin.action(description='Mark selected content as published')
def make_published(modeladmin, request: HttpRequest, queryset):
    queryset.update(blog_status='p')  

@admin.action(description='Withdraw Content')
def withdrawContent(modeladmin, request: HttpRequest, queryset):
    queryset.update(blog_status='w')

# Register your models here.
@admin.register(BlogCategory)
class BlogCategoryAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ["id","category_name","category_url","date"]
    list_display_links = ["id",]
    search_fields = ["id","category_name","category_url","date"]
    list_editable = ["category_name","category_url",]
    fields = (('category_url', 'date'), 'category_name')

@admin.register(Blog)
class BlogAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class  =   BlogAdminResource
    actions = [make_published, make_draft, withdrawContent]
    date_hierarchy = 'blog_date'
    list_display = ["blog_title","blog_author", "blog_status","blog_premium","blog_date",]
    readonly_fields = ['blog_author','blog_id']
    list_display_links = ["blog_title",]
    list_editable = ["blog_status","blog_premium"]
    list_filter = ["blog_status","blog_category","blog_date"]
    list_per_page = 20
    raw_id_fields = ['blog_author','blog_category']
    search_fields = ["blog_id","blog_title", "blog_status","blog_category__category_name","blog_date","blog_author__username"]
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
        js = ["js/prism.js","js/tinymce.js"]
        css = {
        'all': ("css/blog_style.css",)
        }

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'timestamp']
    search_fields = ['id', 'user__username','user__first_name', 'user__last_name','user__email', 'timestamp',]
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
    list_filter = ['query_resolved','date']
    search_fields = ["query_id","customer_email","customer_name","query_subject","date","query_resolved"]
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['id','feature_name','timestamp']
    list_display_links = ["id",]
    search_fields = ["feature_name","feature_image", "feature_details","timestamp",]
    list_editable = ["feature_name"]
    class Media:
        js = ["js/prism.js","js/tinymce.js"]
        css = {
        'all': ("css/blog_style.css",)
        }

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['image_id', 'image','timestamp']
    search_fields = ['image_id', 'image','timestamp']

@admin.register(PaymentDetail)
class PaymentDetailsAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ['id', 'ORDERID' , 'TXNAMOUNT', 'TXNDATE']
    list_display_links = ['id','ORDERID']
    list_filter = ['STATUS','TXNDATE']
    search_fields = ['id','TXNAMOUNT','TXNDATE','RESPCODE','ORDERID']
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    def has_change_permission(self, request: HttpRequest, obj = ...) -> bool:
        return False
    def has_delete_permission(self, request: HttpRequest, obj = ...) -> bool:
        return False

@admin.register(Pricing)
class PriceAdmin(admin.ModelAdmin):
    list_display = ['id','plan_name','plan_price','plan_users']
    list_display_links = ['id', 'plan_name']
    list_editable = ['plan_price']
    search_field = ['id','plan_name','plan_price']
    def has_change_permission(self, request: HttpRequest, obj  = ...) -> bool:
        return request.user.is_superuser
    def has_delete_permission(self, request: HttpRequest, obj = ...) -> bool:
        return request.user.is_superuser
    def has_add_permission(self, request: HttpRequest, obj = ...) -> bool:
        return request.user.is_superuser

@admin.register(PrivacyPolicy)
class PrivacyAdmin(admin.ModelAdmin):
    list_display = ['id','timestamp']
    search_fields = ['timestamp']
    class Media:
        js = ["js/prism.js","js/tinymce.js"]
        css = {
        'all': ("css/blog_style.css",)
        }

@admin.register(TransctionDetail)
class TransactionAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ['order_id','user','amount','timestamp']
    search_fields= ['order_id','user__username','user__first_name', 'user__last_name','user__email','timestamp','status']
    list_filter = ['status','timestamp']
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    def has_change_permission(self, request: HttpRequest, obj = ...) -> bool:
        return False

@admin.register(TermsAndCondition)
class TermsAdmin(admin.ModelAdmin):
    list_display = ['id','timestamp']
    search_fields = ['timestamp']
    class Media:
        js = ["js/prism.js","js/tinymce.js"]
        css = {
        'all': ("css/blog_style.css",)
        }

@admin.register(UserModel)
class UserModelClass(admin.ModelAdmin):
    list_display = ['user','rating_title','star_ratings','testimonial',]
    list_editable = ['testimonial',]
    search_fields = ['id','user__username','user__first_name', 'user__last_name','user__email']
    list_filter = ['testimonial','star_ratings',]
    raw_id_fields = ['user','membership']
    readonly_fields = ['avatar_image','about','ratings','rating_title','star_ratings',]

@admin.register(YoutubeVideo)
class YoutubeVideoAdmin(admin.ModelAdmin):
    list_display = ['video_id','video_title',]
    list_display_links = ['video_id', ]
    search_fields = ['video_id']
    readonly_fields = ['video_title', 'video_description', 'video_thumbnail_default', 'video_thumbnail_medium', 'video_thumbnail_high', 'video_thumbnail_standard',]
    def save_model(self, request, obj, form, change) -> None:
        getYoutubeVideoData(obj,request)
        return super().save_model(request, obj, form, change)
    class Media:
        js = ['js/playerList.js']

@admin.register(YoutubeCoursePlayList)
class YoutubeCourseAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = ['playlist_id','course_title','timestamp']
    list_display_links = ['playlist_id']
    search_fields = ['playlist_id','course_title']
    list_filter = ['timestamp']
    raw_id_fields = ['course_author',]
    readonly_fields = ['course_title','course_description', 'video_thumbnail_default', 'video_thumbnail_medium', 'video_thumbnail_high', 'video_thumbnail_standard', 'videos', 'timestamp']
    def has_add_permission(self, request: HttpRequest) -> bool:
        from .config import config as CONFIG
        return CONFIG.youtube_api_key != None and len(CONFIG.youtube_api_key) != 0
    def has_change_permission(self, request: HttpRequest, obj = ...) -> bool:
        from .config import config as CONFIG
        return CONFIG.youtube_api_key != None and len(CONFIG.youtube_api_key) != 0
    def save_model(self, request, obj, form, change) -> None:
        getPlayListdata(obj,request)
        return super().save_model(request, obj, form, change)
    def delete_model(self, request: HttpRequest, obj: YoutubeCoursePlayList) -> None:
        for item in obj.videos.all():
            item.delete()
        return super().delete_model(request, obj)
    class Media:
        js = ['js/playerList.js']

@admin.register(Configuration)
class SettingConfig(ImportExportMixin,admin.ModelAdmin):
    resource_class = SettingAdminResource
    list_display = ['name','site_name','site_domain']
    fieldsets = (
        ("Site Info" , {
            "fields" : ('site_name','site_domain', 'result_per_page')
        }),
        ("Api Key", {
            "fields" : ('youtube_api_key',)
        }),
        ("Social Links", {
            "fields" : ('instagram','github','youtube','linkedIn','twitter')
        })
    )
    def save_model(self, request, obj, form, change) -> None:
        from . import config
        config.config = obj
        registerPanel(obj.site_name)
        return super().save_model(request, obj, form, change)
    def has_add_permission(self, request: HttpRequest) -> bool:
        return Configuration.objects.all().count() == 0
    def has_delete_permission(self, request: HttpRequest, obj = ...) -> bool:
        return False
    class Media:
        js = ["js/settingConfig.js"]

registerPanel(site_name)
