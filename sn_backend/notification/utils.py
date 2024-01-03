from .models import Notification

from post.models import Post, Comment
from account.models import FriendshipRequest, RelationshipRequest, User
from story.models import ReactStory

def create_notification(request, type_of_notification, post_id=None, friendrequest_id=None, relationship_request_id=None, comment_id=None, story_request_id=None):
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
    elif type_of_notification == 'new_relationship_request':
        relationshiprequest = RelationshipRequest.objects.get(pk=relationship_request_id)
        created_for = relationshiprequest.created_for
        body = f'{request.user.name} đã thiết lập mối quan hệ với bạn'
    # elif type_of_notification == 'accepted_friend_request':
    #     friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
    #     created_for = friendrequest.created_for
    #     body = f'{created_for.name} đã đồng ý lời mời kết bạn'
    # elif type_of_notification == 'accepted_relationship_request':
    #     relationshiprequest = RelationshipRequest.objects.get(pk=relationship_request_id)
    #     created_for = relationshiprequest.created_for
    #     body = f'{created_for.name} đã đồng ý'
    elif type_of_notification == 'tag_comment':
        body = f'{request.user.name} đã nhắc đến bạn trong một bình luận'
        comment = Comment.objects.get(pk=comment_id)
        for tag in comment.tags:
            tag_user = User.objects.get(id=tag['id'])
            created_for = tag_user
    
    if request.user != created_for:
        notification = Notification.objects.create(
            body=body,
            type_of_notification=type_of_notification,
            created_by=request.user,
            post_id=post_id,
            created_for=created_for
        )
        
        if type_of_notification == 'tag_comment':
            comment = Comment.objects.get(pk=comment_id)
            for tag in comment.tags:
                tag_user = User.objects.get(id=tag['id'])
                notification = Notification.objects.create(
                    body=body,
                    type_of_notification=type_of_notification,
                    created_by=request.user,
                    post_id=post_id,
                    created_for=tag_user
                )
                
                return notification