from django.urls import path
from . import api

urlpatterns = [
    path('create/', api.create_group, name='create_group'),
    path('your-groups/', api.get_your_groups, name='get_your_groups'),
    path('discover/', api.get_discover_groups, name='get_discover_groups'),
    path('check-user/<uuid:pk>/', api.check_user_in_group, name='check_user_in_group'),
    path('<uuid:pk>/', api.get_group_detail, name='get_group_detail'),
]