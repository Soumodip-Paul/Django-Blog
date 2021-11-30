# Generated by Django 3.2.9 on 2021-11-30 15:33

from django.conf import settings
from django.db import migrations, models
import make_blog.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('make_blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(default='', max_length=255, unique=True)),
                ('category_url', models.SlugField(max_length=255, unique=True)),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.AlterField(
            model_name='contactclass',
            name='query_subject',
            field=models.CharField(default='', max_length=225),
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('blog_id', models.AutoField(primary_key=True, serialize=False)),
                ('blog_title', models.CharField(default='', max_length=512)),
                ('blog_url', models.SlugField(default='', max_length=512, unique=True)),
                ('blog_content', models.TextField()),
                ('blog_image', models.ImageField(blank=True, default='', null=True, upload_to='blog/image')),
                ('blog_status', models.CharField(choices=[('p', 'published'), ('d', 'draft'), ('w', 'withdrawn')], default='d', max_length=1)),
                ('blog_date', models.DateTimeField()),
                ('blog_author', models.ForeignKey(editable=False, on_delete=models.SET(make_blog.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
                ('blog_category', models.ForeignKey(on_delete=models.SET(make_blog.models.get_sentinel_category), to='make_blog.blogcategory')),
            ],
        ),
    ]
