from rest_framework import serializers

from .models import User, FriendshipRequest, RelationshipRequest, Website

class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ('url','is_private','only_me',)

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ('number','is_private','only_me',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'get_displayed_name', 'email', 'nickname', 'gender', 'friends_count','posts_count','get_avatar','get_cover_image', 'date_joined','relationship_status','partner', 'biography','hometown', 'living_city',)

class UserLessSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email' ,'get_avatar', 'date_joined',)

class FriendshipRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_for = UserSerializer(read_only=True)
    class Meta:
        model = FriendshipRequest
        fields = ('id', 'created_by', 'created_for',)

class RelationshipRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = RelationshipRequest
        fields = ('id', 'created_by', 'relationship_type','created_for',)