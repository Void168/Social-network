from django.forms import ModelForm

from .models import TextStory, StoryAttachment, ReactStory, MediaStory

class TextStoryForm(ModelForm):
    class Meta:
        model = TextStory
        fields = ('body','is_private','only_me','theme','font',)