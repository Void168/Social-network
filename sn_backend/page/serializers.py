from rest_framework import serializers

from .models import Page
from account.serializers import UserSerializer

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        likes = UserSerializer(read_only=True, many=True)
        following = UserSerializer(read_only=True, many=True)
        followers = UserSerializer(read_only=True, many=True)
        fields = ('id', 'name', 'email', 'likes_count','posts_count','get_avatar','get_cover_image', 'created_at','followers_count','page_type', 'biography', 'following', 'followers', 'likes',)

class PageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        likes = UserSerializer(read_only=True, many=True)
        following = UserSerializer(read_only=True, many=True)
        followers = UserSerializer(read_only=True, many=True)
        moderators = UserSerializer(read_only=True, many=True)
        admin = UserSerializer(read_only=True)
        fields = ('id', 'name', 'email', 'phone_number', 'location', 'likes_count','posts_count','get_avatar','get_cover_image', 'created_at','followers_count','page_type', 'biography', 'following', 'followers', 'likes', 'business_hours_status', 'start_time', 'close_time', 'admin', 'moderators',)