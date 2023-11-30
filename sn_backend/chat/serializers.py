from rest_framework import serializers

from account.serializers import UserSerializer

from .models import Conversation, GroupConversation, ConversationMessage, GroupConversationMessage, SeenUser, MessageAttachment, PollOption, GroupPoll, GroupNotification

class SeenUserSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = SeenUser
        fields = ('id', 'created_by', 'created_at_formatted', 'created_at',)
        
class MessageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageAttachment
        fields = ('id', 'get_image',)

class ConversationMessageSerializer(serializers.ModelSerializer):
    sent_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    seen_by = SeenUserSerializer(read_only=True, many=True)
    attachments = MessageAttachmentSerializer(read_only=True, many=True)

    class Meta:
        model = ConversationMessage
        fields = ('id', 'sent_to', 'attachments', 'created_by', 'created_at_formatted', 'body', 'seen_by')
        
class GroupConversationMessageSerializer(serializers.ModelSerializer):
    sent_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    seen_by = SeenUserSerializer(read_only=True, many=True)
    attachments = MessageAttachmentSerializer(read_only=True, many=True)

    class Meta:
        model = GroupConversationMessage
        fields = ('id', 'sent_to', 'attachments', 'created_by', 'created_at_formatted', 'body', 'seen_by')
        
class ConversationSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True, many=True)
    messages = ConversationMessageSerializer(read_only=True, many=True)
    class Meta:
        model = Conversation
        fields = ('id', 'users', 'modified_at_formatted','messages','theme',)

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
        fields = ('content',)