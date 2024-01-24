from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Notification, NotificationForPage
from page.models import Page
from .serializers import NotificationSerializer, NotificationForPageSerializer

@api_view(['GET'])
def notifications(request):
    received_notifications = request.user.received_notifications
    serializer = NotificationSerializer(received_notifications, many=True)

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def page_notifications(request, id):
    page = Page.objects.get(id=id)
    page_received_notifications = NotificationForPage.objects.filter(created_for_id=id)
    
    serializer = NotificationForPageSerializer(page_received_notifications, many=True)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def read_notification(request, pk):
    notification = Notification.objects.filter(created_for=request.user).get(pk=pk)
    notification.is_read = True
    notification.save()
    
    return JsonResponse({'message': 'notification read'})