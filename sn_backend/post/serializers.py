from rest_framework import serializers

from account.serializers import UserSerializer, UserLessSerializer
from page.serializers import PageSerializer
from group.serializers import MemberSerializer
from .models import Post, PostAttachment, Comment, Trend, Like, PageLike, PageComment, MemberComment, MemberLike, GroupPost, PagePost

class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = ('id', 'get_image',)

class LikeSerializer(serializers.ModelSerializer):
    created_by = UserLessSerializer(read_only=True)
    class Meta:
        model = Like
        fields = ('id', 'created_by',)
        
class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id','body','created_by', 'created_at_formatted', 'created_at', 'tags',)
        
class PageLikeSerializer(serializers.ModelSerializer):
    created_by = PageSerializer(read_only=True)
    class Meta:
        model = PageLike
        fields = ('id', 'created_by',)
        
class MemberLikeSerializer(serializers.ModelSerializer):
    created_by = MemberSerializer(read_only=True)
    class Meta:
        model = MemberLike
        fields = ('id', 'created_by',)
        
class PageCommentSerializer(serializers.ModelSerializer):
    created_by = PageSerializer(read_only=True)
    class Meta:
        model = PageComment
        fields = ('id','body','created_by', 'created_at_formatted', 'created_at', 'tags',)
        
class MemberCommentSerializer(serializers.ModelSerializer):
    created_by = MemberSerializer(read_only=True)
    class Meta:
        model = MemberComment
        fields = ('id','body','created_by', 'created_at_formatted', 'created_at', 'tags',)
        
class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    likes = LikeSerializer(read_only=True, many=True)
    post_to = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    page_likes = PageLikeSerializer(read_only=True, many=True)
    page_comments = PageCommentSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ('id', 'body','is_avatar_post', 'is_private','only_me', 'likes_count', 'comments_count', 'comments', 'created_by', 'created_at_formatted', 'created_at', 'attachments','likes', 'post_to','page_likes','page_comments')   

class PagePostSerializer(serializers.ModelSerializer):
    created_by = PageSerializer(read_only=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    likes = LikeSerializer(read_only=True, many=True)
    comments = CommentSerializer(read_only=True, many=True)
    page_likes = PageLikeSerializer(read_only=True, many=True)
    page_comments = PageCommentSerializer(read_only=True, many=True)
    class Meta:
        model = PagePost
        fields = ('id', 'body','is_avatar_post', 'likes_count', 'comments_count', 'comments', 'page_comments', 'created_by', 'created_at_formatted', 'created_at', 'attachments','likes', 'page_likes',)  
        
class GroupPostSerializer(serializers.ModelSerializer):
    created_by = MemberSerializer(read_only=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    likes = MemberLikeSerializer(read_only=True, many=True)
    comments = MemberCommentSerializer(read_only=True, many=True)
    class Meta:
        model = GroupPost
        fields = ('id', 'body', 'likes_count', 'comments_count', 'comments', 'created_by', 'created_at_formatted', 'created_at', 'attachments', 'likes','is_anonymous',)  
        
class AnonymousGroupPostSerializer(serializers.ModelSerializer):
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    likes = MemberLikeSerializer(read_only=True, many=True)
    comments = MemberCommentSerializer(read_only=True, many=True)
    class Meta:
        model = GroupPost
        fields = ('id', 'body', 'likes_count', 'comments_count', 'comments', 'created_at_formatted', 'created_at', 'attachments', 'likes', 'is_anonymous',)  
        
class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    likes = LikeSerializer(read_only=True, many=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    page_likes = PageLikeSerializer(read_only=True, many=True)
    page_comments = PageCommentSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ('id', 'body', 'likes_count', 'likes','comments_count', 'created_by','is_private','only_me', 'created_at_formatted','comments','attachments','page_likes','page_comments',)
        
class PagePostDetailSerializer(serializers.ModelSerializer):
    created_by = PageSerializer(read_only=True)
    comments = PageCommentSerializer(read_only=True, many=True)
    likes = PageLikeSerializer(read_only=True, many=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    page_likes = PageLikeSerializer(read_only=True, many=True)
    page_comments = PageCommentSerializer(read_only=True, many=True)
    class Meta:
        model = PagePost
        fields = ('id', 'body', 'likes_count', 'likes','comments_count', 'created_by','is_private','only_me', 'created_at_formatted','comments','attachments','page_likes','page_comments',)

class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ('id', 'hashtag', 'occurences',)