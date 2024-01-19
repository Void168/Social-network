from django.urls import path

from . import api

urlpatterns = [
    path('create/',api.page_create, name='page_create'),
    path('get-pages/<uuid:id>/',api.get_user_page, name='get_user_page'),
    path('get-page/<uuid:id>/',api.get_page, name='get_page'),
]