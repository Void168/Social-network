from rest_framework import serializers

from account.serializers import UserSerializer

from .models import Conversation, ConversationMessage, SeenUser, MessageAttachment

class SeenUserSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = SeenUser
        fields = ('id', 'created_by', 'created_at_formatted')
        
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
    messages = ConversationMessageSerializer(read_only=True, many=True)
    class Meta:
        model = Conversation
        fields = ('id','admin', 'moderators', 'users', 'modified_at_formatted','messages','theme',)

class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = ConversationMessageSerializer(read_only=True, many=True)
    users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Conversation
        fields = ('id', 'users', 'modified_at_formatted', 'messages','theme',)
    