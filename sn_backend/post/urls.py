from django.urls import path

from . import api

urlpatterns = [
    path('',api.post_list, name='post_list'),
    path('page/<uuid:pk>/',api.page_post_list, name='page_post_list'),
    path('page/profile/<uuid:pk>/',api.page_post_list_profile, name='page_post_list_profile'),
    path('group/<uuid:pk>/',api.get_group_post_list, name='get_group_post_list'),
    path('<uuid:pk>/', api.post_detail, name='post_detail'),
    path('page/<uuid:pk>/detail/', api.page_post_detail, name='page_post_detail'),
    path('<uuid:pk>/like/', api.post_like, name='post_like'),
    path('<uuid:pk>/like-by-user/', api.page_post_like_by_user, name='page_post_like_by_user'),
    path('page/<uuid:id>/<uuid:pk>/like-by-page/', api.page_post_like_by_page, name='page_post_like_by_page'),
    path('<uuid:pk>/comment/', api.post_create_comment, name='post_create_comment'),
    path('page/<uuid:pk>/comment-by-user/', api.page_post_create_comment_by_user, name='page_post_create_comment_by_user'),
    path('page/<uuid:id>/<uuid:pk>/comment-by-page/', api.page_post_create_comment_by_page, name='page_post_create_comment_by_page'),
    path('<uuid:id>/comment/<uuid:pk>/delete/', api.comment_delete, name='comment_delete'),
    path('page/<uuid:id>/comment/<uuid:pk>/delete/', api.page_comment_delete, name='page_comment_delete'),
    path('<uuid:pk>/delete/', api.post_delete, name='post_delete'),
    path('page/<uuid:id>/<uuid:pk>/delete/', api.page_post_delete, name='page_post_delete'),
    path('<uuid:pk>/report/', api.post_report, name='post_report'),
    path('profile/<uuid:id>/', api.post_list_profile, name='post_list_profile'),
    path('profile/<uuid:id>/<uuid:pk>/', api.page_watch_post_list_profile, name='page_watch_post_list_profile'),
    path('profile/<uuid:id>/attachments/', api.post_attachment_list_profile, name='post_attachment_list_profile'),
    path('page/<uuid:id>/attachments/', api.page_post_attachment_list_profile, name='page_post_attachment_list_profile'),
    path('create/', api.post_create, name='post_create'),
    path('create/group/<uuid:pk>/', api.group_post_create, name='group_post_create'),
    path('page/<uuid:pk>/create/', api.page_post_create, name='page_post_create'),
    path('created-to/<uuid:id>/', api.post_created_to, name='post_created_to'),
    path('trends/', api.get_trends, name='get_trends'),
    path('posts-trend-list/',api.posts_trend_list, name='posts_trend_list'),
]
