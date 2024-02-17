from django.urls import path
from . import api

urlpatterns = [
    path('create/', api.create_group, name='create_group'),
    path('your-groups/', api.get_your_groups, name='get_your_groups'),
    path('discover/', api.get_discover_groups, name='get_discover_groups'),
    path('check-user/<uuid:pk>/', api.check_user_in_group, name='check_user_in_group'),
    path('get-current-member/<uuid:pk>/', api.get_current_member, name='get_current_member'),
    path('<uuid:pk>/', api.get_group_detail, name='get_group_detail'),
    path('<uuid:pk>/edit-cover-image/', api.edit_group_cover_image, name='edit_group_cover_image'),
    path('public/<uuid:pk>/join/', api.join_public_group, name='join_public_group'),
    path('<uuid:pk>/join/request/', api.send_join_request_private_group, name='send_join_request_private_group'),
    path('<uuid:pk>/get-join-request/', api.get_join_group_requests, name='get_join_group_requests'),
    path('<uuid:pk>/last-access/', api.update_last_access, name='update_last_access'),
    path('<uuid:pk>/add-moderators/', api.group_add_moderators, name='group_add_moderators'),
    path('<uuid:pk>/remove-moderator/<uuid:id>/', api.remove_moderator, name='remove_moderator'),
    path('<uuid:pk>/add-rule/', api.create_rule, name='create_rule'),
    path('<uuid:pk>/get-rules/', api.get_rules, name='get_rules'),
    path('rule/<uuid:pk>/delete/', api.delete_rule, name='delete_rule'),
    path('<uuid:pk>/get-friends/', api.get_friends_in_group, name='get_friends_in_group'),
    path('<uuid:pk>/user/<uuid:id>/request/<str:status>/', api.handle_join_request, name='handle_join_request'),
    path('<uuid:pk>/info/', api.change_group_info, name='change_group_info'),
    path('<uuid:pk>/website/', api.change_group_website, name='change_group_website'),
    path('<uuid:pk>/show-group/', api.set_show_group, name='set_show_group'),
    path('<uuid:pk>/create-question/', api.create_questions, name='create_questions'),
    path('<uuid:pk>/get-questions/', api.get_group_questions, name='get_group_questions'),
    path('<uuid:pk>/update-question/', api.update_group_question, name='update_group_question'),
    path('<uuid:pk>/answer/', api.create_answer, name='create_answer'),
    path('<uuid:pk>/delete-question/', api.delete_group_question, name='delete_group_question'),
    path('<uuid:pk>/request-join-group/', api.set_request_join_group, name='set_request_join_group'),
    path('<uuid:pk>/kick/<uuid:id>/', api.kick_member, name='kick_member'),
    path('<uuid:pk>/leave/', api.leave_group, name='leave_group'),
    path('<uuid:pk>/set-anonymous-post/', api.set_anonymous_post, name='set_anonymous_post'),
    path('<uuid:pk>/set-anyone-post/', api.set_anyone_can_post, name='set_anyone_can_post'),
    path('<uuid:pk>/set-pending-post/', api.set_pending_post, name='set_pending_post'),
    path('<uuid:pk>/set-anyone-poll/', api.set_anyone_can_poll, name='set_anyone_can_poll'),
    path('<uuid:pk>/overview/', api.get_group_overview, name='get_group_overview'),
    path('<uuid:pk>/growth-join-requests/', api.get_group_join_requests_growth, name='get_group_join_requests_growth'),
    path('<uuid:pk>/growth-posts/', api.get_group_posts_growth, name='get_group_posts_growth'),
    path('<uuid:pk>/growth-likes/', api.get_group_likes_growth, name='get_group_likes_growth'),
    path('<uuid:pk>/growth-comments/', api.get_group_comments_growth, name='get_group_comments_growth'),
    path('<uuid:pk>/growth-active-members/', api.get_group_active_member, name='get_group_active_member'),
]