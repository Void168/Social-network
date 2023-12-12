import uuid

from django.db import models

from account.models import User
from django.utils.timesince import timesince
# Create your models here.
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