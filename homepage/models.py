from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
from django.utils import timezone
import re


# Create your models here.
class User(AbstractUser):
    followed_by = models.ManyToManyField("self", related_name="followers")
    profile = models.CharField(max_length=140)
    
    def clear_search_history(self):
        Search.objects.filter(user_ref=self).delete()

class Tweet(models.Model):
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweets")
    parent_tweet = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="replies")
    date = models.DateTimeField()
    content = models.CharField(max_length=140)
    draft = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)
    retweeted_by = models.ManyToManyField(User, related_name="retweets")
    liked_by = models.ManyToManyField(User, related_name="liked_tweets", through="Like")
    last_hour_likes = models.IntegerField(default=0)

    def save(self, **kwargs):
        if not self.pk:
            self.date = timezone.now()
            if kwargs.get("draft", False):
                self.draft = True
            if not kwargs.get("visible", True):
                self.visible = False
            
            super().save()
            used_tags = re.findall("#[^\s]+", self.content)
            for x in used_tags:
                try:
                    tag = Hashtag.objects.get(text=x)

                except:
                    tag = Hashtag()
                    tag.text = x

                tag.most_recent_use = self.date
                tag.save()
                tag.used_by.add(self)
            
        else:
            super().save()

    def get_last_hour_likes(self):
        current_time = timezone.now()
        one_hour_ago = current_time - timedelta(hours=1)
        likes = self.like_set.filter(timestamp__gte=one_hour_ago, timestamp__lte=current_time)
        return likes.count()


    def toggle_like(self, **kwargs):
        try:
            by = kwargs.get("by")
            if not by == self.user_ref:
                if self.liked_by.filter(id=by.id).exists():
                    print("REMOVE")
                    self.liked_by.remove(by)
                    self.save()
                else:
                    print("ADD")
                    self.liked_by.add(by)
                    print("LIKED_BY")
                    self.save()
                    print("SAVE")
        except Exception as e:
            print(e, "ERROR")
            pass

    def likes (self):
        return self.liked_by.count()

class Search(models.Model):
    user_ref = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=150, null=False, blank=False)
    timestamp = models.DateTimeField()

    def save(self):
        timestamp = timezone.now()
        super().save()


class Hashtag(models.Model):
    text = models.CharField(max_length=140, unique=True)
    used_by = models.ManyToManyField(Tweet, related_name="hashtags")
    most_recent_use = models.DateTimeField()
    trending_score = models.IntegerField(default=0)
    last_hour_likes = models.IntegerField(default=0)

    def total_likes_from_tweets(self):
        total = 0
        for x in self.used_by.all():
            total += x.liked_by.count()
        return total

    def get_trending_score(self):
        current_time = timezone.now()
        one_hour_ago = current_time - timedelta(hours=1)
        last_hour_tweets = Tweet.objects.filter(date__gte=one_hour_ago, date__lte=current_time)
        last_hour_tag_ids = list(last_hour_tweets.exclude(hashtags=None).values_list("hashtags", flat=True))
        matches = last_hour_tag_ids.count(self.id)
        try:
            percent = matches/len(last_hour_tag_ids)
        except:
            percent = 0

        return percent

    def get_last_hour_likes(self):
        current_time = timezone.now()
        one_hour_ago = current_time - timedelta(hours=1)
        total = 0
        for x in self.used_by.filter(date__gte=one_hour_ago, date__lte=current_time)    :
            total += x.last_hour_likes

        return total

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)