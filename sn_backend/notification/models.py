import uuid
from django.db import models

from account.models import User
from post.models import Post
# Create your models here.
class Notification(models.Model):
    NEWFRIENDREQUEST = 'new_friend_request'
    NEWRELATIONSHIPREQUEST = 'new_relationship_request'
    ACCEPTEDFRIENDREQUEST = 'accepted_friend_request'
    ACCEPTEDFRIENDREQUEST = 'accepted_relationship_request'
    REJECTEDFRIENDREQUEST = 'rejected_friend_request'
    REJECTEDFRIENDREQUEST = 'rejected_relationship_request'
    POST_LIKE = 'post_like'
    POST_COMMENT = 'post_comment'
    TAG_COMMENT = 'tag_comment'
    
    CHOICES_TYPE_OF_NOTIFICATION = (
        (NEWFRIENDREQUEST, 'New friendrequest'),
        (ACCEPTEDFRIENDREQUEST, 'Accepted friendrequest'),
        (REJECTEDFRIENDREQUEST, 'Rejected friendrequest'),
        (POST_LIKE, 'Post like'),
        (POST_COMMENT, 'Post comment'),
        (TAG_COMMENT, 'Tag comment'),
        (NEWRELATIONSHIPREQUEST, 'Relationship request'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    type_of_notification = models.CharField(choices=CHOICES_TYPE_OF_NOTIFICATION, max_length=50)
    post = models.ForeignKey(Post, blank=True, null=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="created_notifications", on_delete=models.CASCADE)
    created_for = models.ForeignKey(User, related_name="received_notifications", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_at',)