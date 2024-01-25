from django.forms import ModelForm

from .models import ConversationMessage, GroupConversationMessage, MessageAttachment, Conversation, GroupConversation, GroupPoll, PageMessageAttachment, PageConversationMessage

class MessageForm(ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ('body',)
        
class PageMessageForm(ModelForm):
    class Meta:
        model = PageConversationMessage
        fields = ('body',)

class GroupMessageForm(ModelForm):
    class Meta:
        model = GroupConversationMessage
        fields = ('body',)

class AttachmentForm(ModelForm):
    class Meta:
        model = MessageAttachment
        fields = ('image',)
        
class PageAttachmentForm(ModelForm):
    class Meta:
        model = PageMessageAttachment
        fields = ('image',)

class ChooseThemeForm(ModelForm):
    class Meta:
        model = Conversation
        fields = ('theme',)

class ChooseGroupThemeForm(ModelForm):
    class Meta:
        model = GroupConversation
        fields = ('theme',)
        
class ChangeGroupNameForm(ModelForm):
    class Meta:
        model = GroupConversation
        fields = ('group_name',)

class AvatarGroupForm(ModelForm):
    class Meta:
        model = GroupConversation
        fields = ('avatar',)