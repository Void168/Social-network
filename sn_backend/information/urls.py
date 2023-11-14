from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import api

urlpatterns = [
    path('create/website/', api.website_create, name='website_create'),
    path('<uuid:id>/websites/', api.website_list_profile, name='website_list_profile'),
]
