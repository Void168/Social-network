from django.urls import path
from . import api

urlpatterns = [
    path('create/', api.create_group, name='create_group'),
    path('your-groups/', api.get_your_groups, name='get_your_groups'),
    path('discover/', api.get_discover_groups, name='get_discover_groups'),
    path('check-user/<uuid:pk>/', api.check_user_in_group, name='check_user_in_group'),
    path('<uuid:pk>/', api.get_group_detail, name='get_group_detail'),
    path('public/<uuid:pk>/join/', api.join_public_group, name='join_public_group'),
    path('<uuid:pk>/join/request/', api.send_join_request_private_group, name='send_join_request_private_group'),
    path('<uuid:pk>/get-join-request/', api.get_join_group_requests, name='get_join_group_requests'),
    path('<uuid:pk>/get-friends/', api.get_friends_in_group, name='get_friends_in_group'),
    path('<uuid:pk>/user/<uuid:id>/request/<str:status>/', api.handle_join_request, name='handle_join_request'),
    path('<uuid:pk>/info/', api.change_group_info, name='change_group_info'),
]