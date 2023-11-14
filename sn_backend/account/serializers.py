from rest_framework import serializers

from .models import User, FriendshipRequest, RelationshipRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'friends_count','posts_count','get_avatar','get_cover_image', 'date_joined','relationship_status','partner', 'biography','hometown')
        
class FriendshipRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = FriendshipRequest
        fields = ('id', 'created_by',)

class RelationshipRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = RelationshipRequest
        fields = ('id', 'created_by', 'relationship_type','created_for',)