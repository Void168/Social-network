from rest_framework import serializers

from account.serializers import UserSerializer, UserLessSerializer
from page.serializers import PageSerializer, PageLessSerializer

from .models import Conversation, GroupConversation, ConversationMessage, GroupConversationMessage, SeenUser, SeenPage, MessageAttachment, PollOption, GroupPoll, GroupNotification, PageMessageAttachment, PageConversationMessage

class SeenUserSerializer(serializers.ModelSerializer):
    created_by = UserLessSerializer(read_only=True)
    class Meta:
        model = SeenUser
        fields = ('id', 'created_by', 'created_at_formatted', 'created_at',)
        
class SeenPageSerializer(serializers.ModelSerializer):
    created_by = PageLessSerializer(read_only=True)
    class Meta:
        model = SeenPage
        fields = ('id', 'created_by', 'created_at_formatted', 'created_at',)
        
class MessageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageAttachment
        fields = ('id', 'get_image',)
        
class PageMessageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageMessageAttachment
        fields = ('id', 'get_image',)

class ConversationMessageSerializer(serializers.ModelSerializer):
    sent_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    seen_by = SeenUserSerializer(read_only=True, many=True)
    attachments = MessageAttachmentSerializer(read_only=True, many=True)

    class Meta:
        model = ConversationMessage
        fields = ('id', 'sent_to', 'attachments', 'created_by', 'created_at_formatted', 'body', 'seen_by',)
        
class PageConversationMessageSerializer(serializers.ModelSerializer):
    sent_to = UserLessSerializer(read_only=True)
    sent_to_page = PageLessSerializer(read_only=True)
    created_by = UserLessSerializer(read_only=True)
    created_by_page = PageLessSerializer(read_only=True)
    seen_by = SeenUserSerializer(read_only=True)
    seen_by_page = SeenPageSerializer(read_only=True)
    attachments = MessageAttachmentSerializer(read_only=True, many=True)
    page_attachments = PageMessageAttachmentSerializer(read_only=True, many=True)
    class Meta:
        model = PageConversationMessage
        fields = ('id', 'sent_to', 'sent_to_page', 'attachments', 'page_attachments', 'created_by', 'created_by_page', 'created_at_formatted', 'body', 'seen_by','seen_by_page',)
        
class GroupConversationMessageSerializer(serializers.ModelSerializer):
    sent_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    seen_by = SeenUserSerializer(read_only=True, many=True)
    attachments = MessageAttachmentSerializer(read_only=True, many=True)

    class Meta:
        model = GroupConversationMessage
        fields = ('id', 'sent_to', 'attachments', 'created_by', 'created_at_formatted','created_at', 'body', 'seen_by')
        
class ConversationSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True, many=True)
    messages = ConversationMessageSerializer(read_only=True, many=True)
    class Meta:
        model = Conversation
        fields = ('id', 'users', 'modified_at_formatted','messages','theme',)
        
class PageConversationSerializer(serializers.ModelSerializer):
    user = UserLessSerializer(read_only=True)
    page = PageSerializer(read_only=True)
    page_messages = PageConversationMessageSerializer(read_only=True, many=True)
    class Meta:
        model = Conversation
        fields = ('id', 'user', 'modified_at_formatted','page', 'page_messages',)

class GroupConversationSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)
    moderators = UserSerializer(read_only=True, many=True)
    users = UserSerializer(read_only=True, many=True)
    group_messages = GroupConversationMessageSerializer(read_only=True, many=True)
    class Meta:
        model = GroupConversation
        fields = ('id','group_name', 'admin', 'moderators', 'users', 'get_avatar', 'modified_at_formatted','group_messages','theme',)

class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = ConversationMessageSerializer(read_only=True, many=True)
    users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Conversation
        fields = ('id', 'users', 'modified_at_formatted', 'messages','theme',)

class PollOptionSerializer(serializers.ModelSerializer):
    users_vote = UserSerializer(read_only=True, many=True)
    class Meta:
        model = PollOption
        fields = ('id', 'poll_option_name','users_vote',)

class GroupPollSerializer(serializers.ModelSerializer):
    poll_options = PollOptionSerializer(read_only=True, many=True)
    created_by = UserSerializer(read_only=True)
    group_conversation=GroupConversationSerializer(read_only=True)
    class Meta:
        model = GroupPoll
        fields = ('id','poll_name', 'poll_options','created_at','group_conversation', 'created_by', 'time_end',)

class GroupNotificationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = GroupNotification
        fields = ('id', 'content','created_at',)