import uuid

from django.db import models
from django.utils.timesince import timesince

from account.models import User

# Create your models here.

# class Tag(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     created_by = models.ForeignKey(User, related_name='own_tag', on_delete=models.CASCADE)
#     created_for = models.ForeignKey(User, related_name='tag_for', on_delete=models.CASCADE)
    
class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    tags = models.JSONField('tags', null=True, blank=True, editable=False)
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_at',)
    
    def created_at_formatted(self):
       return timesince(self.created_at)
    
class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='post_attachments')
    created_by = models.ForeignKey(User, related_name='post_attachments', on_delete=models.CASCADE)
    
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        else:
            return ''

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    
    attachments = models.ManyToManyField(PostAttachment, blank=True)
    is_private = models.BooleanField(default=False)
    only_me = models.BooleanField(default=False)
    
    is_avatar_post = models.BooleanField(default=False)
    
    likes = models.ManyToManyField(Like , blank=True)
    likes_count = models.IntegerField(default=0)
    
    comments = models.ManyToManyField(Comment , blank=True)
    comments_count = models.IntegerField(default=0)
    
    reported_by_users = models.ManyToManyField(User, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    
    post_to = models.ForeignKey(User, related_name="post_to", on_delete=models.CASCADE, null=True)
    class Meta:
        ordering = ('-created_at',)
    
    def created_at_formatted(self):
        return timesince(self.created_at)

class Trend(models.Model):
    hashtag = models.CharField(max_length=255)
    occurences = models.IntegerField()