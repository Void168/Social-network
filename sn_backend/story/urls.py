from django.urls import path

from . import api

urlpatterns = [
    path('text-stories/',api.text_story_list, name='text_story_list'),
    path('media-stories/',api.text_story_list, name='text_story_list'),
]
