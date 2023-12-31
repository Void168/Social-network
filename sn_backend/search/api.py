from django.db.models import Q
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from account.serializers import UserSerializer
from post.models import Post
from post.serializers import PostSerializer

@api_view(['POST'])
def search(request):
    data = request.data
    query = data['query']
    current_user = request.user
    
    user_ids = [request.user.id]
    friends = User.objects.get(Q(email=current_user)).friends.all()
        
    for user in User.objects.all():
        user_ids.append(user.id)
        
    
    users = User.objects.filter(name__icontains=query)
    users_serializer = UserSerializer(users, many=True)
        
    posts = Post.objects.filter(Q(body__icontains=query, is_private=False, only_me=False) | Q(created_by__in=list(friends), body__icontains=query, post_to__in=list(user_ids), only_me=False) | Q(created_by__in=list(user_ids), body__icontains=query, post_to__in=list(friends), only_me=False) | Q(created_by__in=list(friends), body__icontains=query, only_me=False))
    
    posts_serializer = PostSerializer(posts, many=True)
    
    return JsonResponse({
        'users': users_serializer.data,
        'posts': posts_serializer.data,
        'query': query,
    }, safe=False)