from django.forms import ModelForm

from .models import TextStory, StoryAttachment, ReactStory, MediaStory

class TextStoryForm(ModelForm):
    class Meta:
        model = TextStory
        fields = ('body','is_private','only_me','theme','font',)

class MediaStoryForm(ModelForm):
    class Meta:
        model = MediaStory
        fields = ('caption','is_private','only_me','theme',)

class StoryAttachmentForm(ModelForm):
    class Meta:
        model = StoryAttachment
        fields = ('image', 'zoom_image', 'rotate')