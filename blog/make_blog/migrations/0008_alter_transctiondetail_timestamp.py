# Generated by Django 3.2.9 on 2021-12-19 11:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('make_blog', '0007_auto_20211219_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transctiondetail',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]