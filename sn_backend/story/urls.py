from django.urls import path

from . import api

urlpatterns = [
    path('text-stories/',api.text_story_list, name='text_story_list'),
    path('media-stories/',api.media_story_list, name='media_story_list'),
    path('create-text-story/',api.create_text_story, name='create_text_story'),
    path('create-media-story/',api.create_media_story, name='create_media_story'),
    path('text-story/<uuid:pk>/delete/',api.text_story_delete, name='text_story_delete'),
    path('get-text-stories/<uuid:id>/', api.user_text_story_list, name='user_text_story_list'),
    path('get-media-stories/<uuid:id>/', api.user_media_story_list, name='user_media_story_list'),
]
