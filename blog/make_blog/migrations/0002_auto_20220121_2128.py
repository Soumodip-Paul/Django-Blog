# Generated by Django 3.2.9 on 2022-01-21 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('make_blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='rating_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='ratings',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='star_ratings',
            field=models.CharField(choices=[('0', 'NO RATING'), ('1', '1 STAR'), ('2', '2 STAR'), ('3', '3 STAR'), ('4', '4 STAR'), ('5', '5 STAR')], default='0', max_length=1),
        ),
    ]
