from django.forms import ModelForm

from .models import ConversationMessage, GroupConversationMessage, MessageAttachment, Conversation

class MessageForm(ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ('body',)

class GroupMessageForm(ModelForm):
    class Meta:
        model = GroupConversationMessage
        fields = ('body',)

class AttachmentForm(ModelForm):
    class Meta:
        model = MessageAttachment
        fields = ('image',)

class ChooseThemeForm(ModelForm):
    class Meta:
        model = Conversation
        fields = ('theme',)