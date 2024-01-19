from django.db.models import Q
from django.http import JsonResponse

from notification.utils import create_notification
from .models import Page
from account.models import User
from rest_framework.decorators import api_view

from .serializers import PageSerializer
from notification.models import Notification
from notification.serializers import NotificationSerializer
from .forms import PageForm

@api_view(['POST'])
def page_create(request):
    form = PageForm(request.POST, request.FILES)

    if form.is_valid():
        page = form.save(commit=False)
        page.admin = request.user
        page.save()
        
        serializer = PageSerializer(page)

        return JsonResponse(serializer.data, safe=False)
    # 'success':'create page successfully'
    else:
        return JsonResponse({'error': 'create page failed'})
