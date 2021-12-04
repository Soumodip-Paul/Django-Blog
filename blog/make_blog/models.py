from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, update_last_login

BLOG_CHOICES = [
    ('d','draft'),
    ('p','published'),
    ('w','withdrawn')
]

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username="nouser")[0]

def get_sentinel_category():
    return BlogCategory.objects.get_or_create(category_url="no_url",category_name="No Category")[0]

# Create your models here.
class ContactClass(models.Model):
    query_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(default='', max_length=255)
    customer_email = models.EmailField()
    query_subject = models.CharField(default='',max_length=225)
    query_desc = models.TextField()
    date = models.DateTimeField()
    def __str__(self) -> str:
        return str(self.query_id) + " " + self.customer_email

class BlogCategory(models.Model):
    category_name = models.CharField(default='',max_length=255,unique=True)
    category_url = models.SlugField(max_length=255,unique=True)
    date = models.DateTimeField()
    def __str__(self) -> str:
        return self.category_url

class Blog(models.Model):
    blog_id = models.AutoField(primary_key=True)
    blog_title = models.CharField(default="",max_length=512)
    blog_url = models.SlugField(default="",max_length=512,unique=True,blank=True, help_text="Leave blank if you donot want custom url")
    blog_image = models.ImageField(upload_to="blog/image", default="", null=True,blank=True)
    blog_status = models.CharField(default='d',max_length=1,choices=BLOG_CHOICES)
    blog_category = models.ForeignKey(BlogCategory,on_delete=models.SET(get_sentinel_category))
    blog_author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user),editable=False)
    blog_date = models.DateTimeField()
    blog_content = models.TextField()
    def __str__(self) -> str:
        return self.blog_url


class UserModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.SET(get_sentinel_user))
    avatar_image = models.ImageField(upload_to="user/images",default="",null=True,blank=True)