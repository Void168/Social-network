from django.db.models import Q
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from account.serializers import UserSerializer
from group.models import Group, Member
from page.models import Page
from post.models import Post, PagePost, GroupPost
from .models import GroupSearchKeyWord, SearchKeyWord
from post.serializers import PostSerializer, PagePostSerializer, GroupPostSerializer, AnonymousGroupPostSerializer
from page.serializers import PageSerializer
from group.serializers import MemberSerializer
from .serializers import GroupSearchKeyWordSerializer

@api_view(['POST'])
def search(request):
    data = request.data
    query = data['query']
    current_user = request.user
    
    user_ids = [request.user.id]
    page_ids = []
    friends = User.objects.get(Q(email=current_user)).friends.all()
        
    for user in User.objects.all():
        user_ids.append(user.id)
        
    for page in Page.objects.all():
        page_ids.append(page.id)
        
    
    users = User.objects.filter(name__icontains=query)
    users_serializer = UserSerializer(users, many=True)
    pages = Page.objects.filter(name__icontains=query)
    pages_serializer = PageSerializer(pages, many=True)
        
    posts = Post.objects.filter(Q(body__icontains=query, is_private=False, only_me=False) | Q(created_by__in=list(friends), body__icontains=query, post_to__in=list(user_ids), only_me=False) | Q(created_by__in=list(user_ids), body__icontains=query, post_to__in=list(friends), only_me=False) | Q(created_by__in=list(friends), body__icontains=query, only_me=False))
    
    posts_serializer = PostSerializer(posts, many=True)
    
    page_posts = PagePost.objects.filter(Q(body__icontains=query) | Q(created_by__in=list(page_ids)))
    page_posts_serializer = PagePostSerializer(page_posts, many=True)
    
    return JsonResponse({
        'pages': pages_serializer.data,
        'users': users_serializer.data,
        'posts': posts_serializer.data,
        'page_posts': page_posts_serializer.data,
        'query': query,
    }, safe=False)
    
@api_view(['POST'])    
def search_group(request, pk):
    group = Group.objects.get(pk=pk)
    query = request.data.get('query')
    current_user = request.user
    
    member_ids = []
    
    for member in group.members.all():
        member_ids.append(member.id)
        
    members = Member.objects.filter(information__name__contains=query)
    members_serializer = MemberSerializer(members, many=True)
        
    group_posts = GroupPost.objects.filter(Q(body__icontains=query, created_by__in=list(member_ids), is_anonymous=False) | Q(created_by__in=list(members), is_anonymous=False))
    
    group_posts_serializer = GroupPostSerializer(group_posts, many=True)
    
    anonymous_group_posts = GroupPost.objects.filter(Q(body__icontains=query, is_anonymous=True))
    anonymous_group_posts_serializer = AnonymousGroupPostSerializer(anonymous_group_posts, many=True)
    
    if members or group_posts or anonymous_group_posts:
        return JsonResponse({
            'members': members_serializer.data,
            'groupPosts': group_posts_serializer.data,
            'anonymousPosts':anonymous_group_posts_serializer.data
        }, safe=False)
    else:
        return JsonResponse({'message': 'Not found'})
    
@api_view(['POST'])  
def create_search_group_keyword(request, pk):
    group = Group.objects.get(pk=pk)
    query = request.data.get('query')
    members = Member.objects.filter(information=request.user)
    
    group_members = group.members.all()
    
    current_member = Member.objects.none()
    
    if members.count() > 0:
        for member in members:
            if member in group_members:
                current_member = member
            else:
                continue
    
    group_keyword = GroupSearchKeyWord.objects.create(
        body=query,
        group=group,
        created_by=current_member
    )
    
    serializer = GroupSearchKeyWordSerializer(group_keyword)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def get_search_group_keywords(request, pk):
    group = Group.objects.get(pk=pk)
    
    members = Member.objects.filter(information=request.user)
    
    group_members = group.members.all()
    
    current_member = Member.objects.none()
    
    if members.count() > 0:
        for member in members:
            if member in group_members:
                current_member = member
            else:
                continue
    
    group_keywords = GroupSearchKeyWord.objects.filter(Q(created_by=current_member, group=group))

    if group_keywords:
        serializer = GroupSearchKeyWordSerializer(group_keywords, many=True)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'message': 'No keywords found'})
    
@api_view(['DELETE'])
def delete_search_group_keywords(request, pk):
    group_keyword = GroupSearchKeyWord.objects.get(pk=pk)
    
    group_keyword.delete()

    return JsonResponse({'message': 'Keyword deleted'})