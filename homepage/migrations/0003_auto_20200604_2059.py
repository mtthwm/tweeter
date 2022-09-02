# Generated by Django 3.0.6 on 2020-06-05 02:59

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_auto_20200508_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 4, 20, 59, 54, 628577)),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='liked_by',
            field=models.ManyToManyField(related_name='liked_tweets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='retweeted_by',
            field=models.ManyToManyField(related_name='retweets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='user_ref',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tweets', to=settings.AUTH_USER_MODEL),
        ),
    ]
