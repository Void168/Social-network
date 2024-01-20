from django.urls import path

from . import api

urlpatterns = [
    path('',api.post_list, name='post_list'),
    path('page/<uuid:pk>/',api.page_post_list, name='page_post_list'),
    path('page/profile/<uuid:pk>/',api.page_post_list_profile, name='page_post_list_profile'),
    path('<uuid:pk>/', api.post_detail, name='post_detail'),
    path('<uuid:pk>/like/', api.post_like, name='post_like'),
    path('<uuid:pk>/comment/', api.post_create_comment, name='post_create_comment'),
    path('comment/<uuid:pk>/delete/', api.comment_delete, name='comment_delete'),
    path('<uuid:pk>/delete/', api.post_delete, name='post_delete'),
    path('<uuid:pk>/report/', api.post_report, name='post_report'),
    path('profile/<uuid:id>/', api.post_list_profile, name='post_list_profile'),
    path('profile/<uuid:id>/attachments', api.post_attachment_list_profile, name='post_attachment_list_profile'),
    path('create/', api.post_create, name='post_create'),
    path('page/<uuid:pk>/create/', api.page_post_create, name='page_post_create'),
    path('created-to/<uuid:id>/', api.post_created_to, name='post_created_to'),
    path('trends/', api.get_trends, name='get_trends'),
    path('posts-trend-list/',api.posts_trend_list, name='posts_trend_list'),
]
