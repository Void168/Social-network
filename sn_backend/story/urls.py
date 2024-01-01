from django.urls import path

from . import api

urlpatterns = [
    path('text-stories/',api.text_story_list, name='text_story_list'),
    path('media-stories/',api.media_story_list, name='media_story_list'),
    path('create-text-story/',api.create_text_story, name='create_text_story'),
    path('create-media-story/',api.create_media_story, name='create_media_story'),
    path('get-detail-text-story/<uuid:pk>/',api.get_detail_text_story, name='get_detail_text_story'),
    path('get-detail-media-story/<uuid:pk>/',api.get_detail_media_story, name='get_detail_media_story'),
    path('seen-text-story/<uuid:pk>/', api.seen_text_story, name='seen_text_story'),
    path('seen-media-story/<uuid:pk>/', api.seen_media_story, name='seen_media_story'),
    path('text-story/<uuid:pk>/delete/',api.text_story_delete, name='text_story_delete'),
    path('media-story/<uuid:pk>/delete/',api.text_media_delete, name='text_media_delete'),
    path('get-text-stories/<uuid:id>/', api.user_text_story_list, name='user_text_story_list'),
    path('get-media-stories/<uuid:id>/', api.user_media_story_list, name='user_media_story_list'),
]
