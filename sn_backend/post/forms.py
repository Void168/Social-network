from django.forms import ModelForm

from .models import Post, PostAttachment

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('body','is_private','only_me','is_avatar_post',)

class AttachmentForm(ModelForm):
    class Meta:
        model = PostAttachment
        fields = ('image',)

class PostToForm(ModelForm):
    class Meta:
        model = Post
        fields = ('body','is_private','post_to',)