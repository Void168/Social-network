from django.forms import ModelForm

from .models import ConversationMessage, MessageAttachment, Conversation

class MessageForm(ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ('body',)

class AttachmentForm(ModelForm):
    class Meta:
        model = MessageAttachment
        fields = ('image',)

class ChooseThemeForm(ModelForm):
    class Meta:
        model = Conversation
        fields = ('theme',)