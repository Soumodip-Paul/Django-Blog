from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.timezone import now
try: from blog.secret import site_name as siteName, smtp_mail as contactEmail
except ImportError : siteName = 'localhost'; contactEmail = 'examle@localhost'
import uuid

BLOG_CHOICES = [
    ('d','draft'),
    ('p','published'),
    ('w','withdrawn')
]

ORDER_STATUS =[
    ('n', 'Payment Not Done'),
    ('f', 'Payment Failed'),
    ('s', 'Success'),
    ('w', 'Payment withdrawn'),
]

STAR_RATING = [
    ('0', 'NO RATING'),
    ('1', '1 STAR'),
    ('2', '2 STAR'),
    ('3', '3 STAR'),
    ('4', '4 STAR'),
    ('5', '5 STAR'),
]

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username="nouser")[0]

def get_sentinel_category():
    return BlogCategory.objects.get_or_create(category_url="no_url",category_name="No Category")[0]

# Create your models here.
class ContactClass(models.Model):
    """ Model to Store User Queries in DataBase """
    query_id = models.AutoField(primary_key=True)
    query_resolved = models.BooleanField(default=False)
    customer_name = models.CharField(default='', max_length=255)
    customer_email = models.EmailField()
    query_subject = models.CharField(default='',max_length=225)
    query_desc = models.TextField()
    date = models.DateTimeField()
    def __str__(self) -> str:
        return str(self.query_id) + " " + self.customer_email

class BlogCategory(models.Model):
    """ Models to create and store Categories of Blogs """
    category_name = models.CharField(default='',max_length=255,unique=True)
    category_url = models.SlugField(max_length=255,unique=True)
    date = models.DateTimeField()
    def __str__(self) -> str:
        return self.category_url

class Blog(models.Model):
    """ Model for Blog Posts to store in Database
        Contains `blog_id`, `blog_title`, `blog_url`, `blog_image`, `blog_status`, `blog_category`, `blog_author`, `blog_date`, `blog_content` Fields
    """
    blog_id = models.AutoField(primary_key=True)
    blog_title = models.CharField(default="",max_length=512)
    blog_url = models.SlugField(default="",max_length=512,unique=True,blank=True, help_text="Leave blank if you donot want custom url")
    blog_image = models.ImageField(upload_to="blog/image/%Y/%m/%d", default="", null=True,blank=True)
    blog_premium = models.BooleanField(default=False,help_text="Mark your blog as premium or not")
    blog_status = models.CharField(default='d',max_length=1,choices=BLOG_CHOICES)
    # blog_category = models.ForeignKey(BlogCategory,on_delete=models.SET_NULL,null=True)
    blog_category = models.ManyToManyField(BlogCategory)
    blog_author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,)
    blog_date = models.DateTimeField()
    blog_content = models.TextField()

    class Meta:
        ordering = ['-blog_date']

    def __str__(self) -> str:
        return self.blog_url

class Feature(models.Model):
    feature_name = models.CharField(default='',max_length=255,unique=True)
    feature_details = models.TextField(default='')
    feature_image = models.FileField(default='',upload_to='feature/image/%Y/%m/%d', validators=[FileExtensionValidator(['jpg', 'png', 'svg'])])
    timestamp = models.DateTimeField(default=now)
    def __str__(self) -> str:
        return self.feature_name

class Image(models.Model):
    """ Model to manage images """
    image_id = models.AutoField(primary_key=True)
    image = models.ImageField(default='',upload_to='blog/image/%Y/%m/%d')
    timestamp = models.DateTimeField(default=now)
    class Meta:
        ordering = ['-timestamp']

    def __str__(self) -> str:
        return str(self.image_id)

class Comment(models.Model):
    """ Model to handle blog comments """
    id = models.AutoField(primary_key=True)
    Text = models.TextField()
    user = models.ForeignKey(User,models.SET_NULL,null=True)
    post = models.ForeignKey(Blog, models.CASCADE)
    parent = models.ForeignKey('self', models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)
    class Meta:
        ordering = ['-timestamp']
    def __str__(self) -> str:
        return str(self.id) + " " + str(self.post)

class PaymentDetail(models.Model):
    id = models.AutoField(primary_key=True)
    BANKNAME=models.CharField(max_length=20)
    BANKTXNID=models.CharField(max_length=20)
    CURRENCY = models.CharField(max_length=4)
    GATEWAYNAME = models.CharField(max_length=20)
    # MID = models.CharField(max_length=30)
    ORDERID = models.CharField(max_length=30)
    PAYMENTMODE = models.CharField(max_length=10)
    RESPCODE = models.CharField(max_length=10)
    RESPMSG = models.CharField(max_length=200)
    STATUS = models.CharField(max_length=10)
    TXNAMOUNT = models.CharField(max_length=10)
    TXNDATE= models.DateTimeField()
    TXNID=models.CharField(max_length=30)
    def save(self, *args, **kwargs):
        if self.pk is None:
            super(PaymentDetail, self).save(*args, **kwargs)
    def __str__(self) -> str:
        return str(self.ORDERID)

class Pricing(models.Model):
    """ Pricing for website """
    plan_name = models.CharField(max_length=50,default="",unique=True)
    plan_price = models.PositiveIntegerField(default=0,unique=True,help_text="All prices in indian rupees")
    plan_desc = models.TextField(default='')
    plan_users = models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.plan_name

class PrivacyPolicy(models.Model):
    page = models.TextField(default='')
    timestamp = models.DateTimeField(default=now)
    def __str__(self) -> str:
        return str(self.id)

class TransctionDetail(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    order_id = models.CharField(max_length=20,default='',unique=True)
    timestamp = models.DateTimeField(default=now)
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default='n')
    """ s : for success
        f : for failure
        n : (Default) for not initiated
    """
    def __str__(self) -> str:
        return self.order_id

class TermsAndCondition(models.Model):
    page = models.TextField(default='')
    timestamp = models.DateTimeField(default=now)
    def __str__(self) -> str:
        return str(self.id)

class UserModel(models.Model):
    """ Extended User Model to store user data other than default Django User Model Fields"""
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    avatar_image = models.ImageField(upload_to="user/images/%Y/%m/%d",default="",null=True,blank=True)
    about = models.TextField(null=True,blank=True)
    membership = models.ForeignKey(Pricing,on_delete=models.SET_NULL,null=True,blank=True,default=1)
    ratings = models.TextField(null=True,blank=True)
    rating_title = models.CharField(max_length=255,null=True,blank=True)
    star_ratings = models.CharField(max_length=1,default='0',choices=STAR_RATING)
    testimonial = models.BooleanField(default=False)
    def __str__(self) -> str:
        return str(self.user)

class YoutubeVideo(models.Model):
    video_id = models.CharField(default='qqee',max_length=255,primary_key=True)
    video_title = models.TextField(default='')
    video_description = models.TextField(default='')
    video_thumbnail_default = models.CharField(default='',max_length=255)
    video_thumbnail_medium = models.CharField(default='',max_length=255)
    video_thumbnail_high = models.CharField(default='',max_length=255)
    video_thumbnail_standard = models.CharField(default='',max_length=255)
    def __str__(self) -> str:
        return self.video_id

class YoutubeCoursePlayList(models.Model):
    playlist_id = models.CharField(default='',max_length=255, primary_key=True)
    course_title = models.TextField(default='')
    course_description = models.TextField(default='')
    course_author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    video_thumbnail_default = models.CharField(default='',max_length=255)
    video_thumbnail_medium = models.CharField(default='',max_length=255)
    video_thumbnail_high = models.CharField(default='',max_length=255)
    video_thumbnail_standard = models.CharField(default='',max_length=255)
    videos = models.ManyToManyField(YoutubeVideo)
    timestamp = models.DateTimeField(default=now)
    def __str__(self) -> str:
        return self.course_title

class Singleton(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(Singleton, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

class Configuration(Singleton):
    name = "Django Configurations"
    site_name = models.CharField(default='Cool Developer',max_length=255,help_text='SITE NAME')
    site_domain = models.CharField(default=siteName,max_length=255,help_text='SITE DOMAIN NAME')
    contact_email = models.EmailField(default=contactEmail, help_text='CONTACT EMAIL ADDRESS')
    result_per_page = models.IntegerField(default=9, help_text='Configure how many query result you want to show in each page ')
    youtube_api_key = models.CharField(null=True,blank=True,max_length=255,help_text="Your Youtube API key")
    instagram = models.CharField(null=True,blank=True,max_length=255,help_text="Your Instagram username")
    github = models.CharField(null=True,blank=True,max_length=255,help_text="Your Github username")
    linkedIn = models.CharField(null=True,blank=True,max_length=255,help_text="Your LinkedIn username")
    twitter = models.CharField(null=True,blank=True,max_length=255,help_text="Your Twitter username")
    youtube = models.CharField(null=True,blank=True,max_length=255,help_text="Your Youtube ChannelId")
    def __str__(self) -> str:
        return self.name