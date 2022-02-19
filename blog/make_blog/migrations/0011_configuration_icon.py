# Generated by Django 3.2.9 on 2022-02-12 10:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('make_blog', '0010_auto_20220211_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='icon',
            field=models.FileField(blank=True, default='', null=True, upload_to='icon/', validators=[django.core.validators.FileExtensionValidator(['ico'])]),
        ),
    ]
