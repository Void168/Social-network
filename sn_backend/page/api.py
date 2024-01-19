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

        return JsonResponse({'success':'create page successfully'})
    else:
        return JsonResponse({'error': 'create page failed'})
    
@api_view(['GET'])
def get_user_page(request, id):
    user = User.objects.get(pk=id)
    
    pages = Page.objects.filter(Q(admin=user) | Q(moderators__in=list([request.user])))
    
    serializer = PageSerializer(pages, many=True)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def get_page(request, id):
    page = Page.objects.get(pk=id)
    
    serializer = PageSerializer(page)
    
    return JsonResponse(serializer.data, safe=False)