from django.db.models import Q
from django.http import JsonResponse

from .pusher import pusher_client
import json

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from post.models import Trend
from account.serializers import UserSerializer, FriendshipRequest

from notification.utils import create_notification

from .forms import PostForm, AttachmentForm
from .models import Post, Comment, Like
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer, LikeSerializer
from notification.serializers import NotificationSerializer

# Create your views here.
@api_view(['GET'])
def post_list(request):
    user_ids = [request.user.id]
    current_user = request.user
    friends = User.objects.get(Q(email=current_user)).friends.all()
    
    for user in request.user.friends.all():
        user_ids.append(user.id)
            
    posts = Post.objects.filter(Q(created_by__in=list(user_ids), only_me=False) | Q(post_to__in=list(friends), only_me=False))
    
    serializer = PostSerializer(posts, many=True)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def posts_trend_list(request):
    user_ids = [request.user.id]
    trend = request.GET.get('trend', '')
        
    for user in User.objects.all():
        user_ids.append(user.id)
        
    posts_trend = Post.objects.filter(created_by__in=list(user_ids))
    
    if trend:
        posts_trend = posts_trend.filter(body__icontains='#' + trend).filter(Q(is_private=False) | Q(only_me=False))
        
    
    serializer = PostSerializer(posts_trend, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def post_detail(request, pk):
    user_ids = [request.user.id]
        
    for user in User.objects.all():
        user_ids.append(user.id)
        
    post= Post.objects.filter(Q(created_by__in=list(user_ids)) | Q(is_private=False) & Q(only_me=False)).get(pk=pk)
    
    return JsonResponse({
        'post': PostDetailSerializer(post).data
    })

@api_view(['GET'])
def post_list_profile(request, id):      
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)
    receivedPosts = Post.objects.filter(post_to=id)

    if not request.user in user.friends.all():
        posts = posts.filter(Q(is_private=False) & Q(only_me=False))
    
    if request.user in user.friends.all():
        posts = posts.filter(only_me=False)
        
    if request.user == user:
        posts = Post.objects.filter(created_by_id=id)
    
    allPosts = posts | receivedPosts
    allPosts.order_by('-created_at')
        
    posts_serializer = PostSerializer(allPosts, many=True)
    user_serializer = UserSerializer(user)

    can_send_friendship_request = True

    if request.user in user.friends.all():
        can_send_friendship_request = False
    
    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if check1 or check2:
        can_send_friendship_request = False
    
    check3 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user).filter(status=FriendshipRequest.REJECTED)
    check4 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user).filter(status=FriendshipRequest.REJECTED)
    
    if check3 or check4:
        can_send_friendship_request = True

    return JsonResponse({
        'posts': posts_serializer.data,
        'user': user_serializer.data,
        'can_send_friendship_request': can_send_friendship_request
    }, safe=False)
    
@api_view(['GET'])
def post_attachment_list_profile(request, id):      
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)
    # receivedPosts = Post.objects.filter(post_to=id)
    post_attachments = []
    
    for post in posts:
        if post.attachments.count() > 0:
            post_attachments.append(post)
        
    serializer = PostSerializer(post_attachments, many=True)

    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def post_create(request):
    form = PostForm(request.POST)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)

    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        if attachment:
            post.attachments.add(attachment)

        user = request.user
        user.posts_count = user.posts_count + 1
        user.save()

        serializer = PostSerializer(post)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add something here later!...'})

@api_view(['POST'])
def post_created_to(request, id):
    receivedUser = User.objects.get(pk=id)
    form = PostForm(request.POST)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)

    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.post_to = receivedUser
        post.save()

        if attachment:
            post.attachments.add(attachment)

        user = request.user
        user.save()

        serializer = PostSerializer(post)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add something here later!...'})
        
@api_view(['POST'])
def post_like(request,pk):
    post =Post.objects.get(pk=pk)
    like = Like.objects.create(created_by=request.user)
    
    if not post.likes.filter(created_by=request.user):
        post =Post.objects.get(pk=pk)
        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()
        
        notification = create_notification(request, 'post_like', post_id=post.id)
        
        serializer_notification = NotificationSerializer(notification)
        
        serializer_data = serializer_notification.data

        json_data = json.dumps(serializer_data)
                
        pusher_client.trigger(f'{request.user.id}-notification', 'like-notification:new', {'notification': json_data})
    
        
        serializer = LikeSerializer(like)
        
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'message': 'post already liked'})
        
@api_view(['POST'])
def post_create_comment(request, pk):
    comment = Comment.objects.create(body=request.data.get('body'), tags=request.data.get('tags'), created_by=request.user)

    post = Post.objects.get(pk=pk)
    post.comments.add(comment)
    post.comments_count = post.comments_count + 1
    post.save()
    
    notification = create_notification(request, 'post_comment', post_id=post.id)
    
    if len(comment.tags) > 0:
        notification_tag = create_notification(request, 'tag_comment', post_id=post.id, comment_id=comment.id)
        
        # serializer_notification_tag_comment = NotificationSerializer(notification_tag)
        
        # serializer_tag_comment_data = serializer_notification_tag_comment.data

        # json_tag_data = json.dumps(serializer_tag_comment_data)
        # pusher_client.trigger(f'{request.user.id}-notification', 'tag-comment-notification:new', {'notification': json_tag_data})
    
    serializer_notification = NotificationSerializer(notification)
        
    serializer_data = serializer_notification.data

    json_data = json.dumps(serializer_data)
                
    pusher_client.trigger(f'{request.user.id}-notification', 'comment-notification:new', {'notification': json_data})
    
    serializer = CommentSerializer(comment)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['DELETE'])
def post_delete(request, pk):
    post = Post.objects.filter(created_by=request.user).get(pk=pk)
    post.delete()
    
    user = request.user
    user.posts_count = user.posts_count - 1
    user.save()
    
    return JsonResponse({'message': 'post deleted'})

@api_view(['POST'])
def post_report(request, pk):
    post = Post.objects.get(pk=pk)
    post.reported_by_users.add(request.user)
    post.save()
    
    return JsonResponse({'message': 'post reported'})

@api_view(['GET'])
def get_trends(request):
    serializer = TrendSerializer(Trend.objects.all(), many=True)

    return JsonResponse(serializer.data, safe=False)