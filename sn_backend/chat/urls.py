from django.urls import path
from . import api

urlpatterns = [
    path('', api.conversation_list, name='conversation_list'),
    path('page/', api.conversation_list, name='page_conversation_list'),
    path('group/', api.group_conversation_list, name='group_conversation_list'),
    path('<uuid:pk>/', api.conversation_detail, name='conversation_detail'),
    path('group/<uuid:pk>/', api.group_conversation_detail, name='group_conversation_detail'),
    path('<uuid:pk>/send/', api.conversation_send_message, name='conversation_send_message'),
    path('<uuid:pk>/pusher/auth/', api.pusher_auth, name='pusher_auth'),
    path('<uuid:pk>/send_group/', api.group_conversation_send_message, name='group_conversation_send_message'),
    path('<uuid:pk>/set_seen/', api.set_seen, name='set_seen'),
    path('<uuid:pk>/group_set_seen/', api.group_set_seen, name='group_set_seen'),
    path('<uuid:pk>/choose_theme/', api.choose_theme, name='choose_theme'),
    path('group/<uuid:pk>/choose_group_theme/', api.choose_group_theme, name='choose_group_theme'),
    path('group/<uuid:pk>/change-group-name/', api.set_group_name, name='set_group_name'),
    path('group/<uuid:pk>/change-group-avatar/', api.set_group_avatar, name='set_group_avatar'),
    path('group/<uuid:pk>/set_moderator/<uuid:user_pk>/', api.set_moderator, name='set_moderator'),
    path('group/<uuid:pk>/kick-user/<uuid:user_pk>/', api.kick_user, name='kick_user'),
    path('group/<uuid:pk>/leave-group/<uuid:user_pk>/', api.leave_group, name='leave_group'),
    path('group/<uuid:pk>/add-users/', api.add_users, name='add_users'),
    path('group/<uuid:pk>/create-poll/', api.create_poll, name='create_poll'),
    path('group/<uuid:conversation_pk>/vote-poll/<uuid:pk>/', api.vote_poll, name='vote_poll'),
    path('group/<uuid:pk>/get-polls/', api.group_polls_list, name='group_polls_list'),
    path('group/<uuid:pk>/delete-poll/', api.delete_poll, name='delete_poll'),
    path('<uuid:pk>/delete/', api.conversation_delete, name='conversation_delete'),
    path('group/<uuid:pk>/delete/', api.group_conversation_delete, name='group_conversation_delete'),
    path('<uuid:user_pk>/get-or-create/', api.conversation_get_or_create, name='conversation_get_or_create'),
    path('<uuid:user_pk>/get-or-create/page/<uuid:id>/', api.page_conversation_get_or_create, name='page_conversation_get_or_create'),
    path('<uuid:pk>/get/', api.conversation_get, name='conversation_get'),
    path('<uuid:user_pk>/get-chat-window/', api.chat_window_detail, name='chat_window_detail'),
    path('<uuid:user_pk>/create/', api.conversation_create, name='conversation_create'),
    path('create-group-chat/', api.group_conversation_create, name='group_conversation_create'),
    path('group/<uuid:pk>/get/', api.group_conversation_get, name='group_conversation_get'),
    path('group/<uuid:pk>/get-notifications/', api.get_group_notifications, name='get_group_notifications'),
]
