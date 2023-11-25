from django.urls import path
from . import api

urlpatterns = [
    path('', api.conversation_list, name='conversation_list'),
    path('group/', api.group_conversation_list, name='group_conversation_list'),
    path('<uuid:pk>/', api.conversation_detail, name='conversation_detail'),
    path('group/<uuid:pk>/', api.group_conversation_detail, name='group_conversation_detail'),
    path('<uuid:pk>/send/', api.conversation_send_message, name='conversation_send_message'),
    path('<uuid:pk>/send_group/', api.group_conversation_send_message, name='group_conversation_send_message'),
    path('<uuid:pk>/set_seen/', api.set_seen, name='set_seen'),
    path('<uuid:pk>/group_set_seen/', api.group_set_seen, name='group_set_seen'),
    path('<uuid:pk>/choose_theme/', api.choose_theme, name='choose_theme'),
    path('<uuid:pk>/delete/', api.conversation_delete, name='conversation_delete'),
    path('<uuid:user_pk>/get-or-create/', api.conversation_get_or_create, name='conversation_get_or_create'),
    path('<uuid:pk>/get/', api.conversation_get, name='conversation_get'),
    path('<uuid:user_pk>/create/', api.conversation_create, name='conversation_create'),
    path('create-group-chat/', api.group_conversation_create, name='group_conversation_create'),
]
