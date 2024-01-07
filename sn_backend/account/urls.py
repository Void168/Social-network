from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import api

urlpatterns = [
    path('me/', api.me, name='me'),
    path('signup/', api.signup, name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-info/<uuid:pk>/', api.user_info, name='user_info'),
    path('edit-profile/', api.edit_profile, name='edit_profile'),
    path('set-biography/', api.set_biography, name='set_biography'),
    path('delete-relationship/', api.delete_relationship, name='delete_relationship'),
    path('edit-cover-image/', api.edit_cover_image, name='edit_cover_image'),
    path('edit-avatar/', api.edit_avatar, name='edit_avatar'),
    path('edit-password/', api.edit_password, name='edit_password'),
    path('friends/<uuid:pk>/', api.friends, name='friends'),
    path('relationship/<uuid:pk>/', api.relationship, name='relationship'),
    path('set-relationship/', api.set_relationship, name='set_relationship'),
    path('set-hometown/', api.set_hometown, name='set_hometown'),
    path('set-livingcity/', api.set_livingcity, name='set_livingcity'),
    path('relationship/<uuid:pk>/request/', api.send_relationship_request, name='send_relationship_request'),
    path('relationship/<uuid:pk>/<str:status>/', api.handle_request_relationship, name='handle_request_relationship'),
    path('friends/suggested/', api.my_friendship_suggestions, name='my_friendship_suggestions'),
    path('delete-friend/<uuid:pk>/', api.delete_friend, name='delete_friend'),
    path('follow/<uuid:pk>/', api.follow, name='follow'),
    path('unfollowed/<uuid:pk>/', api.unfollowed, name='unfollowed'),
    path('friends/<uuid:pk>/request/', api.send_friendship_request, name='send_friendship_request'),
    path('friends/<uuid:pk>/<str:status>/', api.handle_request, name='handle_request'),
]
