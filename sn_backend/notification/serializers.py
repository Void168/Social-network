from rest_framework import serializers

from account.serializers import UserSerializer
from page.serializers import PageSerializer

from post.serializers import PostSerializer

from .models import Notification, NotificationForPage

class NotificationSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_for = UserSerializer(read_only=True)
    created_by_page = PageSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    class Meta:
        model = Notification
        fields = ('id', 'body','type_of_notification', 'post', 'created_for', 'is_read', 'created_at', 'created_by', 'created_by_page',)
        
class NotificationForPageSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_for = PageSerializer(read_only=True)
    created_by_page = PageSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    class Meta:
        model = NotificationForPage
        fields = ('id', 'body','type_of_notification', 'post', 'created_for', 'is_read', 'created_at', 'created_by', 'created_by_page',)