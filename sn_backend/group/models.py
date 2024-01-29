import uuid

from django.db import models
from django.utils import timezone

from account.models import User
from page.models import Page
# Create your models here.
class Rule(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(blank=True, max_length=50)
    body = models.TextField(blank=True)

class Question(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True)
    
class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    information = models.ForeignKey(User, related_name="member_information", on_delete=models.CASCADE)
    date_join_group = models.DateTimeField(default=timezone.now)
    last_access = models.DateTimeField(default=timezone.now)
    
class PageMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    information = models.ForeignKey(Page, related_name="page_member_information", on_delete=models.CASCADE)
    date_join_group = models.DateTimeField(default=timezone.now)
    last_access = models.DateTimeField(default=timezone.now)

class Group(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    email = models.EmailField(blank=True, default='')
    name = models.CharField(blank=True, max_length=50)
    
    cover_image = models.ImageField(upload_to='group_cover_images', blank=True, null=True)
    
    biography = models.CharField(blank=True, default='', max_length=255)
    
    admin = models.ForeignKey(User, related_name='group_admin', on_delete=models.CASCADE)
    moderators = models.ManyToManyField(User, related_name='group_moderators')
    
    members = models.ManyToManyField(Member, related_name='group_members')
    page_members = models.ManyToManyField(PageMember, related_name='group_page_members')
    members_count = models.IntegerField(default=0)
    
    is_private_group = models.BooleanField(default=False)
    show_group = models.BooleanField(default=False)
    
    today_posts_count = models.IntegerField(default=0)
    
    rules = models.ManyToManyField(Rule, related_name='group_rules')
    questions = models.ManyToManyField(Question, related_name='group_quiz')
    
    created_at = models.DateTimeField(default=timezone.now)
    
    def get_cover_image(self):
        if self.cover_image:
            return 'http://127.0.0.1:8000' + self.cover_image.url
        else: 
            return 'https://th.bing.com/th/id/OIP.o1n4kgruF-5cDCCx7jNYKQHaEo?pid=ImgDet&rs=1'
