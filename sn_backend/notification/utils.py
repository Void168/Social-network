from .models import Notification

from post.models import Post
from account.models import FriendshipRequest

def create_notification(request, type_of_notification, post_id=None, friendrequest_id=None):
    created_for = None
    
    if type_of_notification == 'post_like':
        body = f'{request.user.name} đã thích bài viết của bạn'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by
    elif type_of_notification == 'post_comment':
        body = f'{request.user.name} đã bình luận bài viết của bạn'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by
    elif type_of_notification == 'new_friend_request':
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
        body = f'{request.user.name} đã gửi một lời mời kết bạn'
    elif type_of_notification == 'accepted_friend_request':
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
        body = f'{request.user.name} đã đồng ý lời mời kết bạn'
    # elif type_of_notification == 'rejected_friend_request':
    #     friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
    #     created_for = friendrequest.created_for
    #     body = f'{request.user.name} đã từ chối lời mời kết bạn'
    
    notification = Notification.objects.create(
        body=body,
        type_of_notification=type_of_notification,
        created_by=request.user,
        post_id=post_id,
        created_for=created_for
    )
    
    return notification