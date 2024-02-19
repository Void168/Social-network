from django.urls import path

from . import api


urlpatterns = [
    path('', api.search, name='search'),
    path('group/<uuid:pk>/', api.search_group, name='search_group'),
    path('create-key-word/', api.create_search_keyword, name='create_search_keyword'),
    path('get-key-words/', api.get_search_keywords, name='get_search_keywords'),
    path('<uuid:pk>/delete/', api.delete_search_keywords, name='delete_search_keywords'),
    path('group/<uuid:pk>/create-key-word/', api.create_search_group_keyword, name='create_search_group_keyword'),
    path('group/<uuid:pk>/get-key-words/', api.get_search_group_keywords, name='get_search_group_keywords'),
    path('group/<uuid:pk>/delete/', api.delete_search_group_keywords, name='delete_search_group_keywords'),
]