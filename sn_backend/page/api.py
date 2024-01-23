from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm

from notification.utils import create_notification
from .models import Page
from account.models import User
from rest_framework.decorators import api_view

from .serializers import PageSerializer, PageDetailSerializer
from notification.models import Notification
from notification.serializers import NotificationSerializer
from .forms import PageForm, PageBiographyForm, PageTypeForm, PageLocationForm, PageProfileForm

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

@api_view(['GET'])
def get_page_detail(request, id):
    page = Page.objects.get(pk=id)
    
    serializer = PageDetailSerializer(page)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def like_page(request, id):
    current_user = request.user
    page = Page.objects.get(pk=id)
    
    if current_user not in page.likes.all():
        page.followers.add(current_user)
        page.likes.add(current_user)
        
        page.likes_count = page.likes_count + 1
        page.followers_count = page.followers_count + 1
        
        page.save()
    
        return JsonResponse({'success': 'Liked page'})
    else: 
        return JsonResponse({'error': 'Failed'})

@api_view(['POST'])
def edit_page_profile(request, id):
    current_page = Page.objects.get(id=id)
    email = request.data.get('email')
    name = request.data.get('name')
    
    form = PageProfileForm(request.POST, instance=current_page)
        
    if form.is_valid():
        form.save()
        
    serializer = PageSerializer(current_page)
        
    return JsonResponse({'message': 'information updated', 'page': serializer.data})

@api_view(['POST'])
def page_add_moderators(request, id):
    current_page = Page.objects.get(id=id)
    
    other_user_id =request.data.get('otherUser')
    
    users = request.data.get('users')
    for user in users:
        current_page.moderators.add(user)
    
    if other_user_id != "":
        other_user = User.objects.get(id=other_user_id)
    
        current_page.moderators.add(other_user)
    
    current_page.save()
    
    serializer = PageDetailSerializer(current_page)
    
    return JsonResponse({'message':'moderators update'})

@api_view(['POST'])
def set_page_biography(request, id):
    current_page = Page.objects.get(id=id)
        
    form = PageBiographyForm(data=request.POST, instance=current_page)
    
    if form.is_valid():
        form.save()
        
        current_page.save()
    
        serializer = PageSerializer(current_page)
    
        return JsonResponse(serializer.data)
    else: 
        return JsonResponse({'message':'Failed'})

@api_view(['POST'])
def set_page_type(request, id):
    current_page = Page.objects.get(id=id)
    
    form = PageTypeForm(data=request.POST, instance=current_page)
    
    if form.is_valid():
        form.save()
        
        current_page.save()
    
        serializer = PageSerializer(current_page)
    
        return JsonResponse(serializer.data)
    else: 
        return JsonResponse({'message':'Failed'})

@api_view(['POST'])
def set_page_location(request, id):
    current_page = Page.objects.get(id=id)
    
    form = PageLocationForm(data=request.POST, instance=current_page)
    
    if form.is_valid():
        form.save()
        
        current_page.save()
    
        serializer = PageSerializer(current_page)
    
        return JsonResponse(serializer.data)
    else: 
        return JsonResponse({'message':'Failed'})

@api_view(['POST'])
def dislike_page(request, id):
    current_user = request.user
    page = Page.objects.get(pk=id)
    
    if current_user in page.likes.all():
        page.likes.remove(current_user)
        page.likes_count = page.likes_count - 1
        
        if current_user in page.followers.all():
            page.followers.remove(current_user)
            page.followers_count = page.followers_count - 1
        
        page.save()
    
        return JsonResponse({'success': 'Disliked page'})
    else: 
        return JsonResponse({'error': 'Failed'})
    
@api_view(['POST'])
def follow_page(request, id):
    current_user = request.user
    page = Page.objects.get(pk=id)
        
    if current_user not in page.followers.all():
        page.followers.add(current_user)
        page.followers_count = page.followers_count + 1
        
        page.save()
    
        return JsonResponse({'success': 'Followed page'})
    else: 
        return JsonResponse({'error': 'Failed'})
    
@api_view(['POST'])
def unfollow_page(request, id):
    current_user = request.user
    page = Page.objects.get(pk=id)
        
    if current_user in page.followers.all():
        page.followers.remove(current_user)
        page.followers_count = page.followers_count - 1
        
        page.save()
    
        return JsonResponse({'success': 'Unfollowed page'})
    else: 
        return JsonResponse({'error': 'Failed'})
    
@api_view(['POST'])
def delete_page(request, id):
    current_user = request.user
    page = Page.objects.get(pk=id)
    
    form = AuthenticationForm(data=request.POST)

    if form.is_valid() and current_user == page.admin:
        
        page.delete()
        
        return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': form.errors.as_json()}, safe=False)