from django.urls import path
from . import api

urlpatterns = [
    path('', api.conversation_list, name='conversation_list'),
    path('<uuid:pk>/', api.conversation_detail, name='conversation_detail'),
    path('<uuid:pk>/send/', api.conversation_send_message, name='conversation_send_message'),
    path('<uuid:pk>/set_seen/', api.set_seen, name='set_seen'),
    path('<uuid:pk>/delete/', api.conversation_delete, name='conversation_delete'),
    path('<uuid:user_pk>/get-or-create/', api.conversation_get_or_create, name='conversation_get_or_create'),
    path('<uuid:user_pk>/get/', api.conversation_get, name='conversation_get'),
    path('<uuid:user_pk>/create/', api.conversation_create, name='conversation_create'),
]
