from django.db import models
from django.utils import timezone

import uuid
from account.models import User
from group.models import Group, Member
# Create your models here.

class SearchKeyWord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, related_name='user_search_key_word', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ('-created_at',)
    
class GroupSearchKeyWord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    group = models.ForeignKey(Group, related_name="group_search_key_word", on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(Member, related_name='member_search_key_word', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ('-created_at',)