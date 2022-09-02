# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from celery import shared_task

from homepage.models import Tweet

@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="calculate_trending_tweets",
    ignore_result=True
)
def calculate_trending_tweets():
    queryset = Tweet.objects.all()
    print("calculate_trending_tweets")
    print("LOOK HERE")
    for x in queryset:
        x.last_hour_likes = x.get_last_hour_likes()

    Tweet.objects.bulk_update(queryset, ['last_hour_likes'])

@periodic_task(
    run_every=(crontab(minute='*/1')),
    name='calculate_trending_scores',
    ignore_result=True
)
def calculate_trending_tags():
    queryset = Hashtag.objects.all()
    print("calculate_trending_tweets")
    print("LOOK HERE")
    for x in queryset:
        x.last_hour_likes = x.get_last_hour_likes()

    Hashtag.objects.bulk_update(queryset, ['last_hour_likes'])