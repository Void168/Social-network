import uuid

from django.db import models
from django.utils import timezone

from account.models import User
# Create your models here.
class Rule(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(blank=True, max_length=50)
    body = models.TextField(blank=True)

class Question(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True)

class Group(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    email = models.EmailField(blank=True, default='')
    name = models.CharField(blank=True, max_length=50)
    
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    cover_image = models.ImageField(upload_to='cover_images', blank=True, null=True)
    
    biography = models.CharField(blank=True, default='', max_length=255)
    
    admin = models.ForeignKey(User, related_name='group_admin', on_delete=models.CASCADE)
    moderators = models.ManyToManyField(User, related_name='group_moderators')
    
    members = models.ManyToManyField(User, related_name='group_members')
    members_count = models.IntegerField(default=0)
    
    is_private_group = models.BooleanField(default=False)
    
    today_posts_count = models.IntegerField(default=0)
    
    rules = models.ManyToManyField(Rule, related_name='group_rules')
    questions = models.ManyToManyField(Question, related_name='group_quiz')
    
    created_at = models.DateTimeField(default=timezone.now)
