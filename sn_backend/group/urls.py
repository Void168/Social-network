from django.urls import path
from . import api

urlpatterns = [
    path('create/', api.create_group, name='create_group'),
    path('your-groups/', api.get_your_groups, name='get_your_groups'),
    path('<uuid:pk>/', api.get_group_detail, name='get_group_detail'),
]