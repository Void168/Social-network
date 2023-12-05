from rest_framework import serializers

from account.serializers import UserSerializer

from post.serializers import PostSerializer

from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_for = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    class Meta:
        model = Notification
        fields = ('id', 'body','type_of_notification', 'post', 'created_for', 'is_read', 'created_at', 'created_by',)