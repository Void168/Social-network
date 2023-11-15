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

@api_view(['POST'])
def edit_website(request, id):
    user = request.user
    
    website = Website.objects.get(id=id)
    
    form = WebsiteForm(request.POST, instance=website)
        
    if form.is_valid():
        form.save()
        
    serializer = WebsiteSerializer(website)
        
    return JsonResponse({'message': 'information updated', 'website': serializer.data})

@api_view(['DELETE'])
def website_delete(request, pk):
    website = Website.objects.filter(created_by=request.user).get(pk=pk)
    website.delete()
    
    return JsonResponse({'message': 'post deleted'})

@api_view(['GET'])
def phone_number_list_profile(request, id):
    user = User.objects.get(pk=id)
    phone_numbers = PhoneNumber.objects.filter(created_by_id=id)

    if not request.user in user.friends.all():
        phone_numbers = phone_numbers.filter(Q(is_private=False) & Q(only_me=False))
    
    if request.user in user.friends.all():
        phone_numbers = phone_numbers.filter(only_me=False)
        
    if request.user == user:
        phone_numbers = PhoneNumber.objects.filter(created_by_id=id)
        
    phone_numbers_serializer = PhoneNumberSerializer(phone_numbers, many=True)

    return JsonResponse({
        'phone_numbers': phone_numbers_serializer.data,
    }, safe=False)

@api_view(['POST'])
def phone_number_create(request):
    form = PhoneNumberForm(request.POST)

    if form.is_valid():
        phone_number = form.save(commit=False)
        phone_number.created_by = request.user
        phone_number.save()

        serializer = PhoneNumberSerializer(phone_number)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add something here later!...'})