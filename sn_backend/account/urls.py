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
    path('set-relationship/', api.set_relationship, name='set_relationship'),
    path('delete-relationship/', api.delete_relationship, name='delete_relationship'),
    path('edit-cover-image/', api.edit_cover_image, name='edit_cover_image'),
    path('edit-password/', api.edit_password, name='edit_password'),
    path('friends/<uuid:pk>/', api.friends, name='friends'),
    path('friends/suggested/', api.my_friendship_suggestions, name='my_friendship_suggestions'),
    path('friends/<uuid:pk>/request/', api.send_friendship_request, name='send_friendship_request'),
    path('friends/<uuid:pk>/<str:status>/', api.handle_request, name='handle_request'),
]
