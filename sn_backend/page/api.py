from django.db.models import Q
from django.http import JsonResponse

from notification.utils import create_notification
from .models import Page
from account.models import User
from rest_framework.decorators import api_view

from .serializers import PageSerializer
from notification.models import Notification
from notification.serializers import NotificationSerializer

# @api_view(['POST'])
# def page_create(request):