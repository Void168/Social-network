# -*- coding: utf-8 -*-

from os import path, environ
from sys import path as sys_path
from django import setup

from collections import Counter
from datetime import timedelta
from django.utils import timezone

sys_path.append(path.join(path.abspath(path.dirname(__file__)), '..'))
environ.setdefault("DJANGO_SETTINGS_MODULE", 'sn_backend.settings')
setup()

from post.models import Post, Trend

trends = []
def extract_hashtags(text, trends):
    for word in text.split():
        if word[0] == '#':
            trends.append(word[1:])
    
    return trends

for trend in Trend.objects.all():
    trend.delete()

# this_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
# a_week = this_hour - timedelta(hours=144)

# for post in Post.objects.filter(created_at__gte=a_week).filter(is_private=False):
for post in Post.objects.all().filter(is_private=False, only_me=False):
    extract_hashtags(post.body, trends)

for trend in Counter(trends).most_common(10):
    Trend.objects.create(hashtag=trend[0], occurences=trend[1])