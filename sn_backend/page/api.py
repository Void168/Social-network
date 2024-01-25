from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm

from notification.utils import create_notification
from .models import Page
from account.models import User
from rest_framework.decorators import api_view

from .serializers import PageSerializer, PageDetailSerializer
from notification.models import NotificationForPage
from notification.serializers import NotificationSerializer
from .forms import PageForm, PageBiographyForm, PageTypeForm, PageLocationForm, PageProfileForm

from notification.serializers import NotificationForPageSerializer

@api_view(['POST'])
def page_create(request):
    form = PageForm(request.POST, request.FILES)

    if form.is_valid():
        page = form.save(commit=False)
        page.admin = request.user
        page.save()
        
        serializer = PageSerializer(page)

        return JsonResponse({'success':'create page successfully', 'data':serializer.data})
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
    other_page_followers = page.other_page_followers.all()
    other_page_likes = page.other_page_likes.all()
    other_page_following = page.other_page_following.all()
    
    serializer = PageSerializer(page)
    other_page_followers_serializer = PageSerializer(other_page_followers, many=True)
    other_page_likes_serializer = PageSerializer(other_page_likes, many=True)
    other_page_following_serializer = PageSerializer(other_page_following, many=True)
    
    return JsonResponse({
        'data':serializer.data,
        'other_page_followers':other_page_followers_serializer.data,
        'other_page_likes':other_page_likes_serializer.data,
        'other_page_following':other_page_following_serializer.data
    }, safe=False)

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
        
        page_notification = NotificationForPage.objects.create(
            body=f'{request.user.name} đã thích trang của bạn',
            type_of_notification='like_page',
            created_by=request.user,
            created_for=page
        )
    
        return JsonResponse({'success': 'Liked page'})
    else: 
        return JsonResponse({'error': 'Failed'})
    
@api_view(['POST'])
def page_like_page(request, id, pk):
    current_page = Page.objects.get(pk=pk)
    page = Page.objects.get(id=id)
    
    if current_page not in page.other_page_likes.all():
        page.other_page_followers.add(current_page)
        page.other_page_likes.add(current_page)
        
        page.likes_count = page.likes_count + 1
        page.followers_count = page.followers_count + 1
        current_page.followings_count = current_page.followings_count + 1
        page.save()
        current_page.save()
        
        page_notification = NotificationForPage.objects.create(
            body=f'Trang {current_page.name} đã thích trang của bạn',
            type_of_notification='like_page',
            created_by_page=current_page,
            created_for=page
        )
    
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
def page_dislike_page(request, id, pk):
    current_page = Page.objects.get(pk=pk)
    page = Page.objects.get(id=id)
        
    if current_page in page.other_page_likes.all():
        page.other_page_likes.remove(current_page)
        page.likes_count = page.likes_count - 1
        
        if current_page in page.other_page_followers.all():
            page.other_page_followers.remove(current_page)
            page.followers_count = page.followers_count - 1
            
            current_page.other_page_following.remove(page)
            current_page.followings_count = current_page.followings_count - 1
        
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
def page_follow_page(request, id, pk):
    current_page = Page.objects.get(pk=pk)
    page = Page.objects.get(id=id)
        
    if current_page not in page.other_page_followers.all():
        page.other_page_followers.add(current_page)
        page.followers_count = page.followers_count + 1
        
        current_page.other_page_following.add(page)
        current_page.followings_count = page.followings_count + 1
        
        page.save()
        current_page.save()
    
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
def page_unfollow_page(request, id, pk):
    current_page = Page.objects.get(pk=pk)
    page = Page.objects.get(id=id)
        
    if current_page in page.other_page_followers.all():
        page.other_page_followers.remove(current_page)
        page.followers_count = page.followers_count - 1
        
        current_page.other_page_following.remove(page)
        current_page.followings_count = current_page.followings_count - 1
        
        page.save()
        current_page.save()
    
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