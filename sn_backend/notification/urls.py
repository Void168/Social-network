from django.urls import path

from . import api

urlpatterns = [
    path('', api.notifications, name='notifications'),
    path('page/<uuid:id>/', api.page_notifications, name='page_notifications'),
    path('read/<uuid:pk>/', api.read_notification, name='read_notification'),
]
