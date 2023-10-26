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

from account.models import User

users = User.objects.all()

for user in users:
    # Clear the suggestion list
    user.people_you_may_know.clear()


    for friend in user.friends.all():
        for friendsfriend in friend.friends.all():
            if friendsfriend not in user.friends.all() and friendsfriend != user:
                user.people_you_may_know.add(friendsfriend)
        