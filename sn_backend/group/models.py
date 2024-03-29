import uuid

from django.db import models
from django.utils import timezone
from django.utils.timesince import timesince

from account.models import User
from page.models import Page
# Create your models here.
    
class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    information = models.ForeignKey(User, related_name="member_information", on_delete=models.CASCADE)
    date_join_group = models.DateTimeField(default=timezone.now)
    last_access = models.DateTimeField(default=timezone.now)
    
    def last_access_formatted(self):
        return timesince(self.last_access)
    
class PageMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    information = models.ForeignKey(Page, related_name="page_member_information", on_delete=models.CASCADE)
    date_join_group = models.DateTimeField(default=timezone.now)
    last_access = models.DateTimeField(default=timezone.now)

class Group(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    email = models.EmailField(blank=True, default='')
    name = models.CharField(blank=True, max_length=50)
    website = models.CharField(blank=True, max_length=255)
    cover_image = models.ImageField(upload_to='group_cover_images', blank=True, null=True)
    
    biography = models.CharField(blank=True, default='', max_length=255)
    
    admin = models.ForeignKey(User, related_name='group_admin', on_delete=models.CASCADE)
    moderators = models.ManyToManyField(Member, related_name='group_moderators')
    
    members = models.ManyToManyField(Member, related_name='group_members')
    page_members = models.ManyToManyField(PageMember, related_name='group_page_members')
    members_count = models.IntegerField(default=0)
    
    is_private_group = models.BooleanField(default=False)
    show_group = models.BooleanField(default=False)
    anyone_can_join = models.BooleanField(default=True)
    anonymous_post = models.BooleanField(default=False)
    anyone_can_post = models.BooleanField(default=True)
    pending_post = models.BooleanField(default=False)
    anyone_can_poll = models.BooleanField(default=True)
    
    today_posts_count = models.IntegerField(default=0)
    
    ban_list = models.ManyToManyField(Member, related_name='ban_list')
    
    created_at = models.DateTimeField(default=timezone.now)
    
    def created_at_formatted(self):
        return timesince(self.created_at)
    
    def get_cover_image(self):
        if self.cover_image:
            return 'http://127.0.0.1:8000' + self.cover_image.url
        else: 
            return 'https://th.bing.com/th/id/OIP.o1n4kgruF-5cDCCx7jNYKQHaEo?pid=ImgDet&rs=1'

class Rule(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(blank=True, max_length=50)
    created_by = models.ForeignKey(Group, related_name='group_rules', on_delete=models.CASCADE, null=True)
    body = models.TextField(blank=True)

class Question(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(Group, related_name='group_quiz', on_delete=models.CASCADE, null=True)
    body = models.TextField(blank=True)

class Answer(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, related_name='created_answer', on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, related_name="answer_question", on_delete=models.CASCADE)
    body = models.TextField(blank=True)

class JoinGroupRequest(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_for = models.ForeignKey(Group, related_name='received_joingrouprequests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_joingrouprequests', on_delete=models.CASCADE)
    answers = models.ManyToManyField(Answer, related_name="answers")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    
    def created_at_formatted(self):
        return timesince(self.created_at)

