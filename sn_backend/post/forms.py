from django.forms import ModelForm

from .models import Post, PostAttachment, PagePost, PagePostAttachment, MemberPostAttachment, GroupPost, GroupPostPoll

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('body','is_private','only_me','is_avatar_post',)

class PagePostForm(ModelForm):
    class Meta:
        model = PagePost
        fields = ('body', 'is_avatar_post',)
        
class GroupPostForm(ModelForm):
    class Meta:
        model = GroupPost
        fields = ('body', 'is_anonymous',)
        
class AttachmentForm(ModelForm):
    class Meta:
        model = PostAttachment
        fields = ('image',)
        
class PageAttachmentForm(ModelForm):
    class Meta:
        model = PagePostAttachment
        fields = ('image',)
        
class MemberAttachmentForm(ModelForm):
    class Meta:
        model = MemberPostAttachment
        fields = ('image',)

class PostToForm(ModelForm):
    class Meta:
        model = Post
        fields = ('body','is_private','post_to',)