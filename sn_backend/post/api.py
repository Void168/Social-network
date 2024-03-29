from django.db.models import Q
from django.http import JsonResponse

from .pusher import pusher_client
import json
from django.utils.timesince import timesince
from datetime import datetime, timezone, timedelta
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from page.models import Page
from group.models import Group, Member
from account.serializers import UserSerializer, FriendshipRequest
from notification.models import NotificationForPage
from notification.utils import create_notification

from .forms import PostForm, AttachmentForm, PageAttachmentForm, PagePostForm, MemberAttachmentForm, GroupPostForm, SharePostForm
from .models import Post, Comment, Like, Trend, PagePost, PageComment, PageLike, GroupPost, MemberLike, MemberComment, GroupPostPoll, PollOption, SharePost
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer, LikeSerializer, PagePostSerializer, PageLikeSerializer, PageCommentSerializer, PagePostDetailSerializer, GroupPostSerializer, MemberLikeSerializer, MemberCommentSerializer, AnonymousGroupPostSerializer, GroupPostPollSerializer, AnonymousGroupPostPollSerializer, PollOptionSerializer, SharePostSerializer, SharePostDetailSerializer
from notification.serializers import NotificationSerializer, NotificationForPageSerializer

# Create your views here.
@api_view(['GET'])
def post_list(request):
    user_ids = [request.user.id]
    current_user = request.user
    friends = User.objects.get(Q(email=current_user)).friends.all()
    following = User.objects.get(Q(email=current_user)).following.all()
    pages = Page.objects.filter(Q(followers__in=list([request.user])))
    
    for user in request.user.friends.all():
        user_ids.append(user.id)
            
    posts = Post.objects.filter(Q(created_by__in=list(user_ids), only_me=False) | Q(created_by__in=list(following), only_me=False) | Q(post_to__in=list(friends), only_me=False))
    page_posts = PagePost.objects.filter(Q(created_by__in=list(pages)))
    share_posts = SharePost.objects.filter(Q(created_by__in=list(user_ids), only_me=False) | Q(created_by__in=list(following), only_me=False) | Q(post_to__in=list(friends), only_me=False))
    
    post_serializer = PostSerializer(posts, many=True)
    page_posts_serializer = PagePostSerializer(page_posts, many=True)
    share_posts_serializer = SharePostSerializer(share_posts, many=True)
    
    return JsonResponse({
            'posts':post_serializer.data,
            'page_posts': page_posts_serializer.data,
            'share_posts': share_posts_serializer.data,
         }, safe=False)

@api_view(['GET'])
def page_post_list(request, pk):
    current_page = Page.objects.get(pk=pk)
    following = User.objects.get(Q(id=request.user.id)).following.all()
    following_page = current_page.following.all()
            
    posts = Post.objects.filter(Q(created_by__in=list(following), only_me=False, is_private=False) | Q(created_by__in=list(following_page), only_me=False, is_private=False))
    page_posts = PagePost.objects.filter(Q(created_by=current_page))
    
    
    posts_serializer = PostSerializer(posts, many=True)
    page_posts_serializer = PagePostSerializer(page_posts, many=True)
    
    return JsonResponse({
        'posts': posts_serializer.data,
        'page_posts': page_posts_serializer.data
        }, safe=False)

def page_post_list_profile(request, pk):
    current_page = Page.objects.get(pk=pk)
            
    page_posts = PagePost.objects.filter(Q(created_by=current_page))
    
    serializer = PagePostSerializer(page_posts, many=True)
    
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
    
    try:
        post = Post.objects.filter(Q(created_by__in=list(user_ids)) | Q(is_private=False) & Q(only_me=False)).get(pk=pk)
        
        return JsonResponse({
            'post': PostDetailSerializer(post).data
        })
    except Post.DoesNotExist:
        post = SharePost.objects.filter(Q(created_by__in=list(user_ids)) | Q(is_private=False) & Q(only_me=False)).get(pk=pk)
        
        return JsonResponse({
            'post': SharePostDetailSerializer(post).data
        })
    
@api_view(['GET'])
def page_post_detail(request, pk):
    page_post = PagePost.objects.get(pk=pk)
    
    serializer = PagePostDetailSerializer(page_post)
    
    return JsonResponse({
        'page_post': serializer.data
    }, safe=False)

@api_view(['GET'])
def group_post_detail(request, pk):
        
    group_post = GroupPost.objects.get(pk=pk)
    
    return JsonResponse({
        'post': GroupPostSerializer(group_post).data
    })

@api_view(['GET'])
def post_list_profile(request, id):      
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)
    share_posts = SharePost.objects.filter(created_by_id=id)
    receivedPosts = Post.objects.filter(post_to=id)

    if not request.user in user.friends.all():
        posts = posts.filter(Q(is_private=False) & Q(only_me=False))
        share_posts = share_posts.filter(Q(is_private=False) & Q(only_me=False))
    
    if request.user in user.friends.all():
        posts = posts.filter(only_me=False)
        share_posts = share_posts.filter(Q(only_me=False))
        
    if request.user == user:
        posts = Post.objects.filter(created_by_id=id)
        share_posts = share_posts.filter(created_by_id=id)
    
    allPosts = posts | receivedPosts
    allPosts.order_by('-created_at')
        
    posts_serializer = PostSerializer(allPosts, many=True)
    share_posts_serializer = SharePostSerializer(share_posts, many=True)
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
        'share_posts': share_posts_serializer.data,
        'user': user_serializer.data,
        'can_send_friendship_request': can_send_friendship_request
    }, safe=False)
    
@api_view(['GET'])
def page_watch_post_list_profile(request, id, pk):      
    page = Page.objects.get(pk=pk)
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)
    receivedPosts = Post.objects.filter(post_to=id)
    
    if not request.user in user.friends.all() or (user == page.admin or user in page.moderators.all()):
        posts = posts.filter(Q(is_private=False) & Q(only_me=False))
    
    elif request.user in user.friends.all() and user not in page.moderators.all() and user != page.admin:
        posts = posts.filter(only_me=False)
        
    elif request.user == user:
        posts = Post.objects.filter(created_by_id=id)
    
    allPosts = posts | receivedPosts
    allPosts.order_by('-created_at')
        
    posts_serializer = PostSerializer(allPosts, many=True)
    user_serializer = UserSerializer(user)

    return JsonResponse({
        'posts': posts_serializer.data,
        'user': user_serializer.data,
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

@api_view(['GET'])
def page_post_attachment_list_profile(request, id):      
    page = Page.objects.get(pk=id)
    page_posts = PagePost.objects.filter(created_by=page)
    page_post_attachments = []
    
    for page_post in page_posts:
        if page_post.attachments.count() > 0:
            page_post_attachments.append(page_post)
        
    serializer = PagePostSerializer(page_post_attachments, many=True)

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def group_post_attachment_list_profile(request, pk):
    group = Group.objects.get(pk=pk)
    group_posts = GroupPost.objects.filter(group=group)
    # receivedPosts = Post.objects.filter(post_to=id)
    group_post_attachments = []
    
    for group_post in group_posts:
        if group_post.attachments.count() > 0:
            group_post_attachments.append(group_post)
        
    serializer = GroupPostSerializer(group_post_attachments, many=True)

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
def post_update(request, pk):
    post = Post.objects.get(pk=pk)
    
    body = request.data.get('body')
    is_private = request.data.get('is_private')
    only_me = request.data.get('only_me')
    
    post.body = body
    post.is_private = is_private
    post.only_me = only_me
    
    post.save()
    
    serializer = PostSerializer(post)

    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def page_post_create(request, pk):
    page = Page.objects.get(pk=pk)
    form = PagePostForm(request.POST)
    page_attachment = None
    page_attachment_form = PageAttachmentForm(request.POST, request.FILES)

    if page_attachment_form.is_valid():
        page_attachment = page_attachment_form.save(commit=False)
        page_attachment.created_by = page
        page_attachment.save()

    if form.is_valid():
        page_post = form.save(commit=False)
        page_post.created_by = page
        page_post.save()

        if page_attachment:
            page_post.attachments.add(page_attachment)

        page.posts_count = page.posts_count + 1
        page.save()

        serializer = PagePostDetailSerializer(page_post)

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
def create_share_post(request, id):
    post = Post.objects.get(pk=id)
    form = SharePostForm(request.POST)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)

    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if form.is_valid():
        share_post = form.save(commit=False)
        share_post.created_by = request.user
        share_post.post = post
        share_post.save()

        if attachment:
            share_post.attachments.add(attachment)

        user = request.user
        user.posts_count = user.posts_count + 1
        user.save()

        serializer = SharePostSerializer(share_post)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add something here later!...'})
        
@api_view(['POST'])
def post_like(request,pk):
    post = Post.objects.get(pk=pk)
    like = Like.objects.create(created_by=request.user)
    
    if not post.likes.filter(created_by=request.user):
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
        post.likes_count = post.likes_count - 1
        post.likes.remove(like)
        post.save()
        
        serializer = LikeSerializer(like)
        
        return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def page_post_like_by_user(request, pk):
    page_post = PagePost.objects.get(pk=pk)
    
    if not page_post.likes.filter(created_by=request.user):
        like = Like.objects.create(created_by=request.user)
        page_post.likes_count = page_post.likes_count + 1
        page_post.likes.add(like)
        page_post.save()
            
        page_notification = NotificationForPage.objects.create(
            body=f'{request.user.name} đã thích bài viêt trang của bạn',
            type_of_notification='post_like',
            created_by=request.user,
            created_for=page_post.created_by
        )
            
        serializer_notification = NotificationForPageSerializer(page_notification)
        
        serializer = LikeSerializer(like)
            
        return JsonResponse({'data':serializer.data, 'notification':serializer_notification.data}, safe=False)
    else:
        return JsonResponse({'message': 'post already liked'})
    
@api_view(['POST'])
def page_post_like_by_page(request, pk, id):     
    page_post = PagePost.objects.get(pk=pk)
    page = Page.objects.get(id=id)
    
    if not page_post.page_likes.filter(created_by=page):
        page_like = PageLike.objects.create(created_by=page)
        page_post.likes_count = page_post.likes_count + 1
        page_post.page_likes.add(page_like)
        page_post.save()
            
        page_notification = NotificationForPage.objects.create(
            body=f'Trang {page.name} đã thích bài viêt trang của bạn',
            type_of_notification='post_like',
            created_by_page=page,
            created_for=page_post.created_by
        )
            
        serializer_notification = NotificationForPageSerializer(page_notification)
        
        serializer = PageLikeSerializer(page_like)
            
        return JsonResponse({'data':serializer.data, 'notification':serializer_notification.data}, safe=False)
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

@api_view(['POST'])
def page_post_create_comment_by_user(request, pk):
    comment = Comment.objects.create(body=request.data.get('body'), tags=request.data.get('tags'), created_by=request.user)

    page_post = PagePost.objects.get(pk=pk)
    page_post.comments.add(comment)
    page_post.comments_count = page_post.comments_count + 1
    page_post.save()
    
    page_notification = NotificationForPage.objects.create(
            body=f'{request.user.name} đã bình luận bài viêt trang của bạn',
            type_of_notification='post_comment',
            created_by=request.user,
            created_for=page_post.created_by
        )
    
    serializer = CommentSerializer(comment)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def page_post_create_comment_by_page(request, pk, id):
    page = Page.objects.get(id=id)
    page_comment = PageComment.objects.create(body=request.data.get('body'), tags=request.data.get('tags'), created_by=page)

    page_post = PagePost.objects.get(pk=pk)
    page_post.page_comments.add(page_comment)
    page_post.comments_count = page_post.comments_count + 1
    page_post.save()
    
    page_notification = NotificationForPage.objects.create(
            body=f'{page.name} đã bình luận bài viêt trang của bạn',
            type_of_notification='post_comment',
            created_by_page=page,
            created_for=page_post.created_by
        )
    
    serializer = PageCommentSerializer(page_comment)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def group_post_create_comment(request, pk, id):
    members = Member.objects.filter(Q(information=request.user))
    current_member = Member.objects.none()
    group = Group.objects.get(id=id)
    group_members = group.members.all()
    for member in members:
        if member in group_members:
            current_member = member
        else:
            pass
        
    group_post = GroupPost.objects.get(pk=pk)
    group_post_comment = MemberComment.objects.create(body=request.data.get('body'), tags=request.data.get('tags'), created_by=current_member)

    group_post.comments.add(group_post_comment)
    group_post.comments_count = group_post.comments_count + 1
    group_post.save()
    
    # notification = create_notification(request, 'post_comment', post_id=post.id)
    
    # if len(comment.tags) > 0:
    #     notification_tag = create_notification(request, 'tag_comment', post_id=post.id, comment_id=comment.id)
        
        # serializer_notification_tag_comment = NotificationSerializer(notification_tag)
        
        # serializer_tag_comment_data = serializer_notification_tag_comment.data

        # json_tag_data = json.dumps(serializer_tag_comment_data)
        # pusher_client.trigger(f'{request.user.id}-notification', 'tag-comment-notification:new', {'notification': json_tag_data})
    
    # serializer_notification = NotificationSerializer(notification)
        
    # serializer_data = serializer_notification.data

    # json_data = json.dumps(serializer_data)
                
    # pusher_client.trigger(f'{request.user.id}-notification', 'comment-notification:new', {'notification': json_data})
    
    serializer = MemberCommentSerializer(group_post_comment)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['DELETE'])
def comment_delete(request, pk, id):
    post = Post.objects.get(id=id)
    comment = Comment.objects.filter(created_by=request.user).get(pk=pk)
    comment.delete()
    
    post.comments_count = post.comments_count - 1
    post.save()
    
    return JsonResponse({'message': 'comment deleted'})

@api_view(['DELETE'])
def page_comment_delete(request, pk, id):
    page_post = PagePost.objects.get(id=id)
    
    comment = Comment.objects.filter(created_by=request.user).get(pk=pk)
    comment.delete()
    
    page_post.comments_count = page_post.comments_count - 1
    page_post.save()
    
    
    return JsonResponse({'message': 'comment deleted'})

@api_view(['DELETE'])
def post_delete(request, pk):
    post = Post.objects.filter(created_by=request.user).get(pk=pk)
    post.delete()
    
    user = request.user
    user.posts_count = user.posts_count - 1
    user.save()
    
    return JsonResponse({'message': 'post deleted'})

@api_view(['DELETE'])
def page_post_delete(request, pk, id):
    page = Page.objects.get(id=id)
    page_post = PagePost.objects.filter(created_by=page).get(pk=pk)
    page_post.delete()
    
    page.posts_count = page.posts_count - 1
    page.save()
    
    return JsonResponse({'message': 'page post deleted'})

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

@api_view(['POST'])
def group_post_create(request, pk):
    group = Group.objects.get(pk=pk)
    members = Member.objects.filter(Q(information=request.user))
    current_member = Member.objects.none()
    group_members = group.members.all()
    for member in members:
        if member in group_members:
            current_member = member
        else:
            pass
    
    form = GroupPostForm(request.POST)
    
    member_attachment = None
    member_attachment_form = MemberAttachmentForm(request.POST, request.FILES)

    if member_attachment_form.is_valid():
        member_attachment = member_attachment_form.save(commit=False)
        member_attachment.created_by = current_member
        member_attachment.save()

    if form.is_valid():
        group_post = form.save(commit=False)
        group_post.created_by = current_member
        group_post.group = group
        if group.pending_post:
            group_post.pending = True
        else:
            group_post.pending = False
            
        group_post.save()

        if member_attachment:
            group_post.attachments.add(member_attachment)

        if group_post.is_anonymous:
            serializer = GroupPostSerializer(group_post)
            
            return JsonResponse(serializer.data, safe=False)
        else:
            serializer = AnonymousGroupPostSerializer(group_post)

            return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add something here later!...'})

@api_view(['GET'])
def get_your_groups_post_list(request):
    try:
        members = Member.objects.filter(Q(information=request.user))
        groups = Group.objects.none()
        
        for member in members:
            group = Group.objects.filter(members__in=list([member]))
            groups = groups | group
        
        your_group_posts = GroupPost.objects.filter(group__in=list(groups))
        
        serializer = GroupPostSerializer(your_group_posts, many=True)
        return JsonResponse({'data': serializer.data})
    
    except Member.DoesNotExist:
        return JsonResponse({'message': 'No group found'})

@api_view(['GET'])
def get_group_post_list(request, pk):
    
    group = Group.objects.get(pk=pk)

    admin_member = Member.objects.filter(Q(information=group.admin))
    moderators = group.moderators.all()
    
    group_posts = GroupPost.objects.filter(Q(group=group, is_anonymous=False, pending=False) | Q(group=group, created_by__in=admin_member, is_anonymous=False))
    
    if moderators.count() > 0:
        group_posts = GroupPost.objects.filter(Q(group=group, is_anonymous=False, pending=False) | Q(group=group, created_by__in=admin_member, is_anonymous=False) | Q(group=group, created_by__in=moderators, is_anonymous=False))
    
    if group_posts.count() > 0:
        anonymous_group_posts = GroupPost.objects.filter(Q(group=group, is_anonymous=True, pending=False))
        
        serializer = GroupPostSerializer(group_posts, many=True)
        
        anonymous_serializer = AnonymousGroupPostSerializer(anonymous_group_posts, many=True)
        
        return JsonResponse(
            {
                'publicPosts': serializer.data,
                'anonymousPosts': anonymous_serializer.data
            }, safe=False)
    else:
        return JsonResponse(
            {
                'message': 'No posts found'
            })

@api_view(['POST'])
def group_post_like(request, pk, id):
    group_post = GroupPost.objects.get(pk=pk)
    group = Group.objects.get(id=id)
    members = Member.objects.filter(Q(information=request.user))
    group_members = group.members.all()
    current_member = Member.objects.none()
    
    member_like = MemberLike.objects.none()
    for member in members:
        if member in group_members:
            current_member = member
        else:
            pass
    
    current_like = group_post.likes.filter(created_by__in=[current_member])
    if not current_like:
        member_like = MemberLike.objects.create(created_by=current_member)
        group_post.likes_count = group_post.likes_count + 1
        group_post.likes.add(member_like)
        group_post.save()
        
        # notification = create_notification(request, 'post_like', post_id=post.id)
        
        # serializer_notification = NotificationSerializer(notification)
        
        # serializer_data = serializer_notification.data

        # json_data = json.dumps(serializer_data)
                
        # pusher_client.trigger(f'{request.user.id}-notification', 'like-notification:new', {'notification': json_data})
    
        
        serializer = MemberLikeSerializer(member_like)
        
        return JsonResponse({ 'message': 'Liked', 'data':serializer.data }, safe=False)
    else:
        group_post.likes_count = group_post.likes_count - 1
        group_post.likes.remove(current_like[0])
        group_post.save()
                
        return JsonResponse({ 'message': 'Disliked'})

@api_view((['GET']))
def get_pending_posts(request, pk):
    group = Group.objects.get(pk=pk)
    
    admin_member = Member.objects.get(information=group.admin)
    moderators = group.moderators.all()
    
    pending_posts = []
    
    pending_posts = GroupPost.objects.filter(Q(group=group, pending=True)).exclude(Q(created_by=admin_member) | Q(created_by__in=moderators))

    serializer = GroupPostSerializer(pending_posts, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def handle_pending_post(request, pk, status, id):
    group = Group.objects.get(pk=pk)
    pending_post = GroupPost.objects.get(id=id)
    
    timezone_offset = 7.0
    tzinfo = timezone(timedelta(hours=timezone_offset))
    current_time = datetime.now(tzinfo)

    if status == 'accepted':
        pending_post.pending = False
        pending_post.created_at = current_time
        pending_post.created_at_formatted = timesince(current_time)
        
        pending_post.save()
                
        return JsonResponse({'message': 'Post accepted'})
    if status == 'rejected':
        pending_post.delete()

        return JsonResponse({'message': 'Post rejected'})
    
@api_view(['POST'])
def group_post_poll_create(request, pk):
    group = Group.objects.get(pk=pk)
    members = Member.objects.filter(Q(information=request.user))
    current_member = Member.objects.none()
    group_members = group.members.all()
    for member in members:
        if member in group_members:
            current_member = member
        else:
            pass
    body = request.data.get('body')
    options = request.data.get('options')
    allow_add_option = request.data.get('allow_add_option')
    multiple_options = request.data.get('multiple_options')
    is_anonymous = request.data.get('is_anonymous')
    
    group_post_poll = GroupPostPoll.objects.create(
        created_by=current_member,
        group=group,
        body=body,
        allow_add_option=allow_add_option,
        multiple_options=multiple_options,
        is_anonymous=is_anonymous
    )
    
    for option_value in options:
        # print(option_value)
        option = PollOption.objects.create(
            body=option_value,
            created_by=current_member
        )
        
        group_post_poll.options.add(option)
    
        group_post_poll.save()

    if group_post_poll.is_anonymous:
        serializer = AnonymousGroupPostPollSerializer(group_post_poll)
            
        return JsonResponse(serializer.data, safe=False)
    else:
        serializer = GroupPostPollSerializer(group_post_poll)

        return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def add_poll_option(request, pk, id):
    group_post_polls = GroupPostPoll.objects.get(pk=pk)
    group = Group.objects.get(id=id)
    additional_option_body = request.data.get('additional_option')
    
    members = Member.objects.filter(Q(information=request.user))
    current_member = Member.objects.none()
    group_members = group.members.all()
    for member in members:
        if member in group_members:
            current_member = member
        else:
            pass
    
    option = PollOption.objects.create(
            body=additional_option_body,
            created_by=current_member
        )
    
    group_post_polls.options.add(option)
    group_post_polls.save()
    
    serializer = PollOptionSerializer(option)
    
    return JsonResponse({'option': serializer.data}, safe=False)

@api_view(['GET'])
def get_group_post_poll(request, pk):
    group = Group.objects.get(pk=pk)
    
    # group_post_polls = GroupPostPoll.objects.filter(group=group)
    group_post_polls = GroupPostPoll.objects.all()
    
    serializer = GroupPostPollSerializer(group_post_polls, many=True)

    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def vote_poll(request, pk, id):
    option = PollOption.objects.get(pk=pk)
    
    members = Member.objects.filter(Q(information=request.user))
    current_member = Member.objects.none()
    group = Group.objects.get(id=id)
    group_members = group.members.all()
    for member in members:
        if member in group_members:
            current_member = member
        else:
            pass
        
    if current_member not in option.vote_by.all():
        option.vote_by.add(current_member)
        option.votes_count = option.votes_count + 1
        option.save()
        
        return JsonResponse({'message': 'voted'})
    else:
        option.vote_by.remove(current_member)
        option.votes_count = option.votes_count - 1
        option.save()
        
        return JsonResponse({'message': 'Remove vote'})

@api_view(['GET'])
def check_vote(request, pk):
    option = PollOption.objects.get(pk=pk)
    if not option.vote_by.filter(Q(information=request.user)):
        return JsonResponse({'message': 'Not voted yet'})
    else:
        return JsonResponse({'message': 'voted'})
    
@api_view(['DELETE'])
def delete_poll(request, pk):
    group_post_poll = GroupPostPoll.objects.get(pk=pk)
    
    if group_post_poll.created_by.information == request.user:
        group_post_poll.delete()

        return JsonResponse({'message': 'Poll deleted'})
    else:
        return JsonResponse({'message': 'Delete poll failed'})
    
@api_view(['DELETE'])
def delete_group_post(request, pk, id):
    group_post = GroupPost.objects.get(pk=pk)
    group = Group.objects.get(id=id)
    moderators = group.moderators.all()
    
    current_member = Member.objects.none()
    group_members = group.members.all()
    for member in members:
        if member in group_members:
            current_member = member
        else:
            pass
    
    if group_post.created_by.information == request.user or request.user == group.admin.information or current_member.information == request.user:
        group_post.delete()

        return JsonResponse({'message': 'Group post deleted'})
    else:
        return JsonResponse({'message': 'Group post delete failed'})
