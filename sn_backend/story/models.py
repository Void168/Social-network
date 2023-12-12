import uuid

from django.db import models
from django.core.validators import MaxValueValidator

from account.models import User
from django.utils.timesince import timesince
# Create your models here.
class StoryAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='story_attachments_image', null=True)
    video = models.FileField(upload_to='story_attachments_video', null=True)
    created_by = models.ForeignKey(User, related_name='story_attachments', on_delete=models.CASCADE)
    
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        else:
            return ''
    def get_video(self):
        if self.video:
            return 'http://127.0.0.1:8000' + self.video.url
        else:
            return ''

class TextStory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True)
    font = models.TextField(blank=True, default='Đơn giản', max_length=50)
    theme = models.CharField(blank=True, default='Cổ điển', max_length=50)
    
    created_by = models.ForeignKey(User, related_name='text_story', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    duaration = models.IntegerField(default=10)
    
    is_private = models.BooleanField(default=False)
    only_me = models.BooleanField(default=False)
    
    seen_by = models.ManyToManyField(User, related_name='seen_text_story')
    seen_count = models.IntegerField(default=0)
    
    def created_at_formatted(self):
        return timesince(self.created_at)

class MediaStory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    caption = models.TextField(blank=True, null=True)
    attachments = models.ManyToManyField(StoryAttachment, blank=True)
    font = models.TextField(blank=True, default='Đơn giản', max_length=50)
    theme = models.CharField(blank=True, max_length=50)
    
    created_by = models.ForeignKey(User, related_name='media_story', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    duaration = models.IntegerField(MaxValueValidator(10))
    
    is_private = models.BooleanField(default=False)
    only_me = models.BooleanField(default=False)
    
    seen_by = models.ManyToManyField(User, related_name='seen_media_story')
    seen_count = models.IntegerField(default=0)
    
    def created_at_formatted(self):
        return timesince(self.created_at)