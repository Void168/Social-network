from django.db.models import Q
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from account.serializers import UserSerializer

from .forms import WebsiteForm, PhoneNumberForm
from .models import Website, PhoneNumber
from .serializers import WebsiteSerializer, PhoneNumberSerializer

@api_view(['GET'])
def website_list_profile(request, id):
    user = User.objects.get(pk=id)
    websites = Website.objects.filter(created_by_id=id)

    if not request.user in user.friends.all():
        websites = websites.filter(Q(is_private=False) & Q(only_me=False))
    
    if request.user in user.friends.all():
        websites = websites.filter(only_me=False)
        
    if request.user == user:
        websites = Website.objects.filter(created_by_id=id)
        
    websites_serializer = WebsiteSerializer(websites, many=True)

    return JsonResponse({
        'websites': websites_serializer.data,
    }, safe=False)
    
@api_view(['POST'])
def website_create(request):
    form = WebsiteForm(request.POST)

    if form.is_valid():
        website = form.save(commit=False)
        website.created_by = request.user
        website.save()

        serializer = WebsiteSerializer(website)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add something here later!...'})