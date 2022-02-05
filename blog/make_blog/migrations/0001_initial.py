# Generated by Django 3.2.9 on 2022-02-04 18:46

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('blog_id', models.AutoField(primary_key=True, serialize=False)),
                ('blog_title', models.CharField(default='', max_length=512)),
                ('blog_url', models.SlugField(blank=True, default='', help_text='Leave blank if you donot want custom url', max_length=512, unique=True)),
                ('blog_image', models.ImageField(blank=True, default='', null=True, upload_to='blog/image/%Y/%m/%d')),
                ('blog_premium', models.BooleanField(default=False, help_text='Mark your blog as premium or not')),
                ('blog_status', models.CharField(choices=[('d', 'draft'), ('p', 'published'), ('w', 'withdrawn')], default='d', max_length=1)),
                ('blog_date', models.DateTimeField()),
                ('blog_content', models.TextField()),
                ('blog_author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-blog_date'],
            },
        ),
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(default='', max_length=255, unique=True)),
                ('category_url', models.SlugField(max_length=255, unique=True)),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ContactClass',
            fields=[
                ('query_id', models.AutoField(primary_key=True, serialize=False)),
                ('query_resolved', models.BooleanField(default=False)),
                ('customer_name', models.CharField(default='', max_length=255)),
                ('customer_email', models.EmailField(max_length=254)),
                ('query_subject', models.CharField(default='', max_length=225)),
                ('query_desc', models.TextField()),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='EditableSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='Cool Developer', help_text='SITE NAME', max_length=255)),
                ('site_domain', models.CharField(default='localhost:8000', help_text='SITE DOMAIN NAME', max_length=255)),
                ('contact_email', models.EmailField(default='paulsoumo64@gmail.com', help_text='CONTACT EMAIL ADDRESS', max_length=254)),
                ('result_per_page', models.IntegerField(default=9, help_text='Configure how many query result you want to show in each page ')),
                ('youtube_api_key', models.CharField(blank=True, help_text='Your Youtube API key', max_length=255, null=True)),
                ('instagram', models.CharField(blank=True, help_text='Your Instagram username', max_length=255, null=True)),
                ('github', models.CharField(blank=True, help_text='Your Github username', max_length=255, null=True)),
                ('linkedIn', models.CharField(blank=True, help_text='Your LinkedIn username', max_length=255, null=True)),
                ('twitter', models.CharField(blank=True, help_text='Your Twitter username', max_length=255, null=True)),
                ('youtube', models.CharField(blank=True, help_text='Your Youtube ChannelId', max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_name', models.CharField(default='', max_length=255, unique=True)),
                ('feature_details', models.TextField(default='')),
                ('feature_image', models.FileField(default='', upload_to='feature/image/%Y/%m/%d', validators=[django.core.validators.FileExtensionValidator(['jpg', 'png', 'svg'])])),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('image_id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(default='', upload_to='blog/image/%Y/%m/%d')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='PaymentDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('BANKNAME', models.CharField(max_length=20)),
                ('BANKTXNID', models.CharField(max_length=20)),
                ('CURRENCY', models.CharField(max_length=4)),
                ('GATEWAYNAME', models.CharField(max_length=20)),
                ('ORDERID', models.CharField(max_length=30)),
                ('PAYMENTMODE', models.CharField(max_length=10)),
                ('RESPCODE', models.CharField(max_length=10)),
                ('RESPMSG', models.CharField(max_length=200)),
                ('STATUS', models.CharField(max_length=10)),
                ('TXNAMOUNT', models.CharField(max_length=10)),
                ('TXNDATE', models.DateTimeField()),
                ('TXNID', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(default='', max_length=50, unique=True)),
                ('plan_price', models.PositiveIntegerField(default=0, help_text='All prices in indian rupees', unique=True)),
                ('plan_desc', models.TextField(default='')),
                ('plan_users', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PrivacyPolicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.TextField(default='')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='TermsAndCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.TextField(default='')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='YoutubeVideo',
            fields=[
                ('video_id', models.CharField(default='qqee', max_length=255, primary_key=True, serialize=False)),
                ('video_title', models.TextField(default='')),
                ('video_description', models.TextField(default='')),
                ('video_thumbnail_default', models.CharField(default='', max_length=255)),
                ('video_thumbnail_medium', models.CharField(default='', max_length=255)),
                ('video_thumbnail_high', models.CharField(default='', max_length=255)),
                ('video_thumbnail_standard', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='YoutubeCoursePlayList',
            fields=[
                ('playlist_id', models.CharField(default='', max_length=255, primary_key=True, serialize=False)),
                ('course_title', models.TextField(default='')),
                ('course_description', models.TextField(default='')),
                ('video_thumbnail_default', models.CharField(default='', max_length=255)),
                ('video_thumbnail_medium', models.CharField(default='', max_length=255)),
                ('video_thumbnail_high', models.CharField(default='', max_length=255)),
                ('video_thumbnail_standard', models.CharField(default='', max_length=255)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('videos', models.ManyToManyField(to='make_blog.YoutubeVideo')),
            ],
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('avatar_image', models.ImageField(blank=True, default='', null=True, upload_to='user/images/%Y/%m/%d')),
                ('about', models.TextField(blank=True, null=True)),
                ('ratings', models.TextField(blank=True, null=True)),
                ('rating_title', models.CharField(blank=True, max_length=255, null=True)),
                ('star_ratings', models.CharField(choices=[('0', 'NO RATING'), ('1', '1 STAR'), ('2', '2 STAR'), ('3', '3 STAR'), ('4', '4 STAR'), ('5', '5 STAR')], default='0', max_length=1)),
                ('testimonial', models.BooleanField(default=False)),
                ('membership', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='make_blog.pricing')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TransctionDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=0)),
                ('order_id', models.CharField(default='', max_length=20, unique=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('n', 'Payment Not Done'), ('f', 'Payment Failed'), ('s', 'Success'), ('w', 'Payment withdrawn')], default='n', max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Text', models.TextField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='make_blog.comment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='make_blog.blog')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AddField(
            model_name='blog',
            name='blog_category',
            field=models.ManyToManyField(to='make_blog.BlogCategory'),
        ),
    ]
