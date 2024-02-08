from django.db.models import Q
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from account.serializers import UserSerializer
from group.models import Group, Member
from page.models import Page
from post.models import Post, PagePost, GroupPost
from post.serializers import PostSerializer, PagePostSerializer, GroupPostSerializer
from page.serializers import PageSerializer
from group.serializers import MemberSerializer

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
    data = request.data
    query = data['query']
    current_user = request.user
    
    member_ids = []
    
    for member in group.members.all():
        member_ids.append(member.id)
        
    members = Member.objects.filter(information__name__contains=query)
    members_serializer = MemberSerializer(members, many=True)
        
    group_posts = GroupPost.objects.filter(Q(body__icontains=query, created_by__in=list(member_ids)) | Q(created_by__in=list(members), is_anonymous=False))
    
    group_posts_serializer = GroupPostSerializer(group_posts, many=True)
    
    return JsonResponse({
        'members': members_serializer.data,
        'groupPosts': group_posts_serializer.data,
    }, safe=False)