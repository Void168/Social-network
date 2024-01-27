from rest_framework import serializers

from .models import Page
from account.serializers import UserSerializer

class PageSerializer(serializers.ModelSerializer):
    likes = UserSerializer(read_only=True, many=True)
    following = UserSerializer(read_only=True, many=True)
    followers = UserSerializer(read_only=True, many=True)
    class Meta:
        model = Page
        fields = ('id', 'name', 'email', 'is_page', 'location', 'likes_count','posts_count','get_avatar','get_cover_image', 'created_at','followers_count','page_type', 'biography', 'following', 'followers', 'likes', 'followings_count')
        
class PageLessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'name', 'email', 'is_page', 'likes_count','posts_count','get_avatar', 'created_at','followers_count','page_type', 'followings_count')

class PageDetailSerializer(serializers.ModelSerializer):
    likes = UserSerializer(read_only=True, many=True)
    following = UserSerializer(read_only=True, many=True)
    followers = UserSerializer(read_only=True, many=True)
    moderators = UserSerializer(read_only=True, many=True)
    admin = UserSerializer(read_only=True)
    
    class Meta:
        model = Page
        fields = ('id', 'name', 'email', 'is_page', 'location', 'likes_count','posts_count','get_avatar','get_cover_image', 'created_at','followers_count','page_type', 'biography', 'following', 'followers', 'likes', 'business_hours_status', 'start_time', 'close_time', 'admin', 'moderators',)