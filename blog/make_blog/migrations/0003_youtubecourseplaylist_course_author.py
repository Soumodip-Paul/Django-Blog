# Generated by Django 3.2.9 on 2022-02-05 18:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('make_blog', '0002_rename_editablesetting_configuration'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtubecourseplaylist',
            name='course_author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
