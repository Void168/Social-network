from django.urls import path

from . import api

urlpatterns = [
    path('create/',api.page_create, name='page_create'),
    path('get-pages/<uuid:id>/',api.get_user_page, name='get_user_page'),
    path('get-page/<uuid:id>/',api.get_page, name='get_page'),
    path('get-page/<uuid:id>/detail/',api.get_page_detail, name='get_page_detail'),
    path('<uuid:id>/like/',api.like_page, name='like_page'),
    path('edit-profile-page/<uuid:id>/', api.edit_page_profile, name='edit_page_profile'),
    path('set-biography/<uuid:id>/', api.set_page_biography, name='set_page_biography'),
    path('set-type/<uuid:id>/', api.set_page_type, name='set_page_type'),
    path('set-location/<uuid:id>/', api.set_page_location, name='set_page_location'),
    path('<uuid:id>/dislike/',api.dislike_page, name='dislike_page'),
    path('<uuid:id>/follow/',api.follow_page, name='follow_page'),
    path('<uuid:id>/unfollow/',api.unfollow_page, name='unfollow_page'),
]