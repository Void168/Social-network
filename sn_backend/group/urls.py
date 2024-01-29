from django.urls import path
from . import api

urlpatterns = [
    path('create/', api.create_group, name='create_group'),
]