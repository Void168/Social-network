from django.urls import path

from . import api


urlpatterns = [
    path('', api.search, name='search'),
    path('group/<uuid:pk>/', api.search_group, name='search_group'),
]