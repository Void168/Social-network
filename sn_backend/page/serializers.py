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
