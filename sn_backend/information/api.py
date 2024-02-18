from django.db.models import Q
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from account.serializers import UserSerializer

from page.models import Page
from page.serializers import PageSerializer

from .forms import WebsiteForm, PhoneNumberForm, PageWebsiteForm, PagePhoneNumberForm
from .models import Website, PhoneNumber, PageWebsite, PagePhoneNumber
from .serializers import WebsiteSerializer, PhoneNumberSerializer, PageWebsiteSerializer, PagePhoneNumberSerializer

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
    
    return JsonResponse({'message': 'website deleted'})

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

@api_view(['POST'])
def edit_phone_number(request, id):
    user = request.user
    
    phone_number = PhoneNumber.objects.get(id=id)
    
    form = PhoneNumberForm(request.POST, instance=phone_number)
        
    if form.is_valid():
        form.save()
        
    serializer = PhoneNumberSerializer(phone_number)
        
    return JsonResponse({'message': 'information updated', 'phone_number': serializer.data})

@api_view(['DELETE'])
def phone_number_delete(request, pk):
    phone_number = PhoneNumber.objects.filter(created_by=request.user).get(pk=pk)
    phone_number.delete()
    
    return JsonResponse({'message': 'phone number deleted'})

@api_view(['GET'])
def page_website_list_profile(request, id):
    page = Page.objects.get(pk=id)
    page_websites = PageWebsite.objects.filter(created_by=page)
        
    page_websites_serializer = PageWebsiteSerializer(page_websites, many=True)

    return JsonResponse({
        'websites': page_websites_serializer.data,
    }, safe=False)
    
@api_view(['POST'])
def page_website_create(request, id):
    page = Page.objects.get(pk=id)
    form = PageWebsiteForm(request.POST)

    if form.is_valid():
        page_website = form.save(commit=False)
        page_website.created_by = page
        page_website.save()

        serializer = PageWebsiteSerializer(page_website)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add something here later!...'})

@api_view(['POST'])
def edit_page_website(request, id, pk):
    page = Page.objects.get(pk=pk)
    user = request.user
    
    page_website = Website.objects.get(id=id)
    
    form = WebsiteForm(request.POST, instance=page_website)
        
    if form.is_valid():
        if user == page.admin or user in page.moderators.all():
            form.save()
        
    serializer = PageWebsiteSerializer(page_website)
        
    return JsonResponse({'message': 'information updated', 'website': serializer.data})

@api_view(['DELETE'])
def page_website_delete(request, pk, id):
    user = request.user
    page = Page.objects.get(pk=pk)
    if user == page.admin or user in page.moderators.all():
        page_website = PageWebsite.objects.filter(created_by=page).get(id=id)
        page_website.delete()
    
        return JsonResponse({'message': 'website deleted'})

@api_view(['GET'])
def page_phone_number_list_profile(request, id):
    page = Page.objects.get(pk=id)
    page_phone_numbers = PagePhoneNumber.objects.filter(created_by=page)
        
    page_phone_numbers_serializer = PagePhoneNumberSerializer(page_phone_numbers, many=True)

    return JsonResponse({
        'phone_numbers': page_phone_numbers_serializer.data,
    }, safe=False)

@api_view(['POST'])
def page_phone_number_create(request, id):
    page = Page.objects.get(pk=id)
    form = PagePhoneNumberForm(request.POST)
    if form.is_valid():
        page_phone_number = form.save(commit=False)
        page_phone_number.created_by = page
        page_phone_number.save()

        serializer = PagePhoneNumberSerializer(page_phone_number)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add something here later!...'})

@api_view(['POST'])
def edit_page_phone_number(request, id, pk):
    page = Page.objects.get(pk=pk)
    user = request.user
    
    page_phone_number = PhoneNumber.objects.get(id=id)
    
    form = PagePhoneNumberForm(request.POST, instance=phone_number)
        
    if form.is_valid():
        if user == page.admin or user in page.moderators.all():
            form.save()
        
    serializer = PhoneNumberSerializer(page_phone_number)
        
    return JsonResponse({'message': 'information updated', 'page_phone_number': serializer.data})

@api_view(['DELETE'])
def page_phone_number_delete(request, pk, id):
    user = request.user
    page = Page.objects.get(pk=pk)
    
    if user == page.admin or user in page.moderators.all():
        page_phone_number = PagePhoneNumber.objects.filter(created_by=page).get(id=id)
        page_phone_number.delete()
    
        return JsonResponse({'message': 'phone number deleted'})
    