from django.forms import ModelForm

from .models import ConversationMessage, GroupConversationMessage, MessageAttachment, Conversation, GroupConversation

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

class ChooseGroupThemeForm(ModelForm):
    class Meta:
        model = GroupConversation
        fields = ('theme',)