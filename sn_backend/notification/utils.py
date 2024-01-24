from .models import Notification, NotificationForPage

from post.models import Post, Comment, PagePost, PageComment
from account.models import FriendshipRequest, RelationshipRequest, User
from page.models import Page
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

def create_notification_by_page(request, type_of_notification, post_id=None, page_id=None, comment_id=None, story_request_id=None):
    created_for = None
    page = Page.objects.get(id=page_id)
    if type_of_notification == 'post_like':
        body = f'{page.name} đã thích bài viết của bạn'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by
    elif type_of_notification == 'post_comment':
        body = f'{page.name} đã bình luận bài viết của bạn'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by
    # elif type_of_notification == 'accepted_friend_request':
    #     friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
    #     created_for = friendrequest.created_for
    #     body = f'{created_for.name} đã đồng ý lời mời kết bạn'
    # elif type_of_notification == 'accepted_relationship_request':
    #     relationshiprequest = RelationshipRequest.objects.get(pk=relationship_request_id)
    #     created_for = relationshiprequest.created_for
    #     body = f'{created_for.name} đã đồng ý'
    elif type_of_notification == 'tag_comment':
        body = f'{page.name} đã nhắc đến bạn trong một bình luận'
        comment = Comment.objects.get(pk=comment_id)
        for tag in comment.tags:
            tag_user = User.objects.get(id=tag['id'])
            created_for = tag_user
    
    if request.user != created_for:
        notification = Notification.objects.create(
            body=body,
            type_of_notification=type_of_notification,
            created_by=page,
            post_id=post_id,
            created_for=created_for
        )
        
        if type_of_notification == 'tag_comment':
            comment = Comment.objects.get(pk=comment_id)
            for tag in comment.tags:
                tag_page = Page.objects.get(id=tag['id'])
                notification = PageNotification.objects.create(
                    body=body,
                    type_of_notification=type_of_notification,
                    created_by=request.user,
                    post_id=post_id,
                    created_for=tag_page
                )
                
                return notification

def create_page_notification_by_user(request, type_of_notification, post_id=None, comment_id=None, story_request_id=None):
    created_for = None
    if type_of_notification == 'tag_comment':
        body = f'{request.user.name} đã nhắc đến trang của bạn trong một bình luận'
        comment = Comment.objects.get(pk=comment_id)
        for tag in comment.tags:
            tag_page = Page.objects.get(id=tag['id'])
            created_for = tag_page
    if request.user != created_for:
        notification = NotificationForPage.objects.create(
            body=body,
            type_of_notification=type_of_notification,
            created_by=request.user,
            created_by_page=page,
            post_id=post_id,
            created_for=created_for
        )
        
        if type_of_notification == 'tag_comment':
            page_comment = PageComment.objects.get(pk=comment_id)
            for tag in page_comment.tags:
                tag_user = User.objects.get(id=tag['id'])
                notification = Notification.objects.create(
                    body=body,
                    type_of_notification=type_of_notification,
                    created_by=page,
                    post_id=post_id,
                    created_for=tag_user
                )
                
                return notification
        
def create_page_notification_by_page(request, type_of_notification, post_id=None, comment_id=None, story_request_id=None, page_id=None):
        page = Page.objects.get(id=page_id)
        if type_of_notification == 'post_like':
            body = f'{page.name} đã thích bài viết trang của bạn'
            page_post = PagePost.objects.get(pk=post_id)
            created_for = page_post.created_by
        elif type_of_notification == 'post_comment':
            body = f'{page.name} đã bình luận bài viết trang của bạn'
            page_post = PagePost.objects.get(pk=post_id)
            created_for = page_post.created_by
        elif type_of_notification == 'tag_comment':
            body = f'{page.name} đã nhắc đến trang của bạn trong một bình luận'
            comment = Comment.objects.get(pk=comment_id)
            for tag in comment.tags:
                tag_page = Page.objects.get(id=tag['id'])
                created_for = tag_page
        if page != created_for:
            notification = NotificationForPage.objects.create(
                body=body,
                type_of_notification=type_of_notification,
                created_by_page=page,
                post_id=post_id,
                created_for=created_for
            )