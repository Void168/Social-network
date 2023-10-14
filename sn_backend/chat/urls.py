from django.urls import path
from . import api

urlpatterns = [
    path('', api.conversation_list, name='conversation_list'),
]
