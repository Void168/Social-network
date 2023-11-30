import uuid

from django.db import models
from django.utils.timesince import timesince
from django.utils import timezone

from account.models import User
# Create your models here.
 
class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    theme = models.CharField(blank=True, default='Cổ điển', max_length=50)
    
    def modified_at_formatted(self):
        return timesince(self.created_at)

class GroupConversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(default = '', max_length=255)
    group_name = models.TextField(default = '', max_length=255)
    users = models.ManyToManyField(User, related_name='group_conversations')
    avatar = models.ImageField(upload_to='group_avatars', blank=True, null=True)
    admin = models.ForeignKey(User, related_name='admin_groupchat', on_delete=models.CASCADE)
    moderators = models.ManyToManyField(User, related_name='moderators_groupchat')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    theme = models.CharField(blank=True, default='Cổ điển', max_length=50)
    
    def modified_at_formatted(self):
        return timesince(self.created_at)
    
    def get_avatar(self):
        if self.avatar:
            return 'http://127.0.0.1:8000' + self.avatar.url

class SeenUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='see_user', on_delete=models.CASCADE)
    
    def created_at_formatted(self):
        return timesince(self.created_at)

class MessageAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='message_attachments')
    created_by = models.ForeignKey(User, related_name='message_attachments', on_delete=models.CASCADE)
    
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        else:
            return ''

class ConversationMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    attachments = models.ManyToManyField(MessageAttachment, blank=True)
    sent_to = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    is_latest_message = models.BooleanField(default=False)
    seen_by = models.ManyToManyField(SeenUser, related_name='seen_message')
    
    def created_at_formatted(self):
        return timesince(self.created_at)

class GroupNotification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(blank=True)
    group_conversation = models.ForeignKey(GroupConversation, related_name='group_notifications', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

class GroupConversationMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_conversation = models.ForeignKey(GroupConversation, related_name='group_messages', on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    attachments = models.ManyToManyField(MessageAttachment, blank=True)
    sent_to = models.ForeignKey(User, related_name='group_received_messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='group_sent_messages', on_delete=models.CASCADE)
    is_latest_message = models.BooleanField(default=False)
    seen_by = models.ManyToManyField(SeenUser, related_name='group_seen_message')
    
    def created_at_formatted(self):
        return timesince(self.created_at)
    
class PollOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poll_option_name = models.CharField(default = '', max_length=255)
    users_vote = models.ManyToManyField(User, related_name='users_vote', null=True)

class GroupPoll(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_conversation = models.ForeignKey(GroupConversation, related_name='group_poll',null=True, on_delete=models.CASCADE)
    poll_name = models.TextField(default = '', max_length=255)
    poll_options = models.ManyToManyField(PollOption, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='user_create_poll', on_delete=models.CASCADE)
    time_end = models.DateTimeField()
    