from django.urls import path

from . import api

urlpatterns = [
    path('create/',api.page_create, name='page_create'),
    path('get-pages/<uuid:id>/',api.get_user_page, name='get_user_page'),
    path('get-page/<uuid:id>/',api.get_page, name='get_page'),
    path('get-page/<uuid:id>/detail/',api.get_page_detail, name='get_page_detail'),
    path('<uuid:id>/like/',api.like_page, name='like_page'),
    path('<uuid:pk>/like/<uuid:id>/',api.page_like_page, name='page_like_page'),
    path('edit-profile-page/<uuid:id>/', api.edit_page_profile, name='edit_page_profile'),
    path('<uuid:id>/add-moderators/', api.page_add_moderators, name='page_add_moderators'),
    path('<uuid:pk>/edit-avatar/', api.edit_page_avatar, name='edit_page_avatar'),
    path('<uuid:pk>/edit-cover-image/', api.edit_page_cover_image, name='edit_page_cover_image'),
    path('set-biography/<uuid:id>/', api.set_page_biography, name='set_page_biography'),
    path('set-type/<uuid:id>/', api.set_page_type, name='set_page_type'),
    path('set-location/<uuid:id>/', api.set_page_location, name='set_page_location'),
    path('<uuid:id>/dislike/',api.dislike_page, name='dislike_page'),
    path('<uuid:pk>/dislike/page/<uuid:id>/',api.page_dislike_page, name='page_dislike_page'),
    path('<uuid:id>/follow/',api.follow_page, name='follow_page'),
    path('following/',api.get_user_following_pages, name='get_user_following_pages'),
    path('<uuid:pk>/follow/page/<uuid:id>/',api.page_follow_page, name='page_follow_page'),
    path('<uuid:id>/unfollow/',api.unfollow_page, name='unfollow_page'),
    path('<uuid:pk>/unfollow/page/<uuid:id>/',api.page_unfollow_page, name='page_unfollow_page'),
    path('delete/<uuid:id>/',api.delete_page, name='delete_page'),
]