# Generated by Django 3.0.8 on 2020-07-16 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0011_auto_20200611_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='hashtag',
            name='last_hour_likes',
            field=models.IntegerField(default=0),
        ),
    ]