from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import api

urlpatterns = [
    path('create/website/', api.website_create, name='website_create'),
    path('<uuid:id>/websites/', api.website_list_profile, name='website_list_profile'),
    path('<uuid:id>/edit-website/', api.edit_website, name='edit_website'),
    path('<uuid:pk>/delete/website/', api.website_delete, name='website_delete'),
    path('create/phone-number/', api.phone_number_create, name='website_create'),
    path('<uuid:id>/phone-numbers/', api.phone_number_list_profile, name='phone_number_list_profile'),
    path('<uuid:id>/edit-phone-number/', api.edit_phone_number, name='edit_phone_number'),
    path('<uuid:pk>/delete/phone-number/', api.phone_number_delete, name='phone_number_delete'),
    path('page/<uuid:id>/create/website/', api.page_website_create, name='page_website_create'),
    path('page/<uuid:id>/websites/', api.page_website_list_profile, name='page_website_list_profile'),
    path('page/<uuid:pk>/edit-website/<uuid:id>/', api.edit_page_website, name='edit_page_website'),
    path('page/<uuid:pk>/delete/website/<uuid:id>/', api.page_website_delete, name='page_website_delete'),
    path('page/<uuid:id>/create/phone-number/', api.page_phone_number_create, name='page_phone_number_create'),
    path('page/<uuid:id>/phone-numbers/', api.page_phone_number_list_profile, name='page_phone_number_list_profile'),
    path('page/<uuid:pk>/edit-phone-number/<uuid:id>/', api.edit_page_phone_number, name='edit_page_phone_number'),
    path('page/<uuid:pk>/delete/phone-number/<uuid:id>/', api.page_phone_number_delete, name='page_phone_number_delete'),
]
