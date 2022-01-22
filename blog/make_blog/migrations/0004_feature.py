# Generated by Django 3.2.9 on 2022-01-22 08:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('make_blog', '0003_usermodel_testimonial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_name', models.CharField(default='', max_length=255)),
                ('feature_details', models.TextField(default='')),
                ('feature_image', models.ImageField(default='', upload_to='feature/image/%Y/%m/%d')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
