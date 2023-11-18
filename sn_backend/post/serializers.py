from rest_framework import serializers

from account.serializers import UserSerializer

from .models import Post, PostAttachment, Comment, Trend, Like

class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = ('id', 'get_image',)

# class TagSerializer(serializers.ModelSerializer):
#     created_by = UserSerializer(read_only=True)
#     created_for = UserSerializer(read_only=True)
#     class Meta:
#         model = Tag
#         fields = ('id', 'created_by','created_for')

class LikeSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Like
        fields = ('id', 'created_by',)
class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    # tags = TagSerializer(read_only=True, many=True)
    class Meta:
        model = Comment
        fields = ('id','body','created_by', 'created_at_formatted','tags',)
        
class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    likes = LikeSerializer(read_only=True, many=True)
    post_to = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ('id', 'body','is_private','only_me', 'likes_count', 'comments_count', 'comments', 'created_by', 'created_at_formatted', 'attachments','likes', 'post_to',)   
        
        
class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    likes = LikeSerializer(read_only=True, many=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ('id', 'body', 'likes_count', 'likes','comments_count', 'created_by','is_private','only_me', 'created_at_formatted','comments','attachments',)

class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ('id', 'hashtag', 'occurences',)