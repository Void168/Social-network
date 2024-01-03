from rest_framework import serializers

from account.serializers import UserSerializer

from .models import TextStory, StoryAttachment, MediaStory, ReactStory

class StoryAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryAttachment
        fields = ('id', 'get_image', 'get_video', 'zoom_image', 'rotate',)

class ReactStorySerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = ReactStory
        fields = ('id', 'created_by', 'type_of_react',)

class TextStorySerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    seen_by = UserSerializer(read_only=True, many=True)
    class Meta:
        model = TextStory
        fields = ('id', 'body', 'is_private', 'only_me', 'seen_by', 'font', 'theme', 'created_by', 'created_at_formatted', 'created_at',)

class MediaStorySerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    attachments = StoryAttachmentSerializer(read_only=True, many=True)
    seen_by = UserSerializer(read_only=True, many=True)
    class Meta:
        model = MediaStory
        fields = ('id', 'is_private', 'caption', 'attachments', 'only_me', 'theme', 'seen_by', 'created_by', 'created_at_formatted', 'created_at',)

class TextStoryDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    reacted_by = ReactStorySerializer(read_only=True, many=True)
    seen_by = UserSerializer(read_only=True, many=True)
    class Meta:
        model = TextStory
        fields = ('id', 'body', 'font', 'is_private', 'only_me', 'theme', 'seen_count', 'seen_by', 'created_by', 'created_at_formatted','duaration', 'reacted_by', 'created_at',)  

class MediaStoryDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    attachments = StoryAttachmentSerializer(read_only=True, many=True)
    reacted_by = ReactStorySerializer(read_only=True, many=True)
    seen_by = UserSerializer(read_only=True, many=True)
    class Meta:
        model = MediaStory
        fields = ('id', 'caption', 'attachments', 'font', 'theme', 'created_by', 'created_at_formatted', 'duaration', 'is_private', 'only_me', 'reacted_by', 'seen_by', 'seen_count', 'created_at')