from django.urls import path

from . import api

urlpatterns = [
    path('create/',api.page_create, name='page_create'),
]