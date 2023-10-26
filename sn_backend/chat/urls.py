from django.urls import path
from . import api

urlpatterns = [
    path('', api.conversation_list, name='conversation_list'),
    path('<uuid:pk>/', api.conversation_detail, name='conversation_detail'),
    path('<uuid:pk>/get_last_message/', api.get_last_message, name='get_last_message'),
    path('<uuid:pk>/send/', api.conversation_send_message, name='conversation_send_message'),
    path('<uuid:user_pk>/get-or-create/', api.conversation_get_or_create, name='conversation_get_or_create'),
]
