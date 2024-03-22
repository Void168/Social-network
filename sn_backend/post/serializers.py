from rest_framework import serializers

from account.serializers import UserSerializer, UserLessSerializer
from page.serializers import PageSerializer
from group.serializers import MemberSerializer, GroupSerializer
from .models import Post, PostAttachment, Comment, Trend, Like, PageLike, PageComment, MemberComment, MemberLike, GroupPost, PagePost, PollOption, GroupPostPoll, SharePost

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
        fields = ('id', 'created_by', 'created_at',)
        
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

class PollOptionSerializer(serializers.ModelSerializer):
    created_by = MemberSerializer(read_only=True)
    vote_by = MemberSerializer(read_only=True, many=True)
    class Meta:
        model = PollOption
        fields = ('id', 'body', 'created_by', 'vote_by', 'votes_count',)  
        
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

class PostLessSerializer(serializers.ModelSerializer):
    created_by = UserLessSerializer(read_only=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    post_to = UserLessSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'body', 'is_private','only_me', 'created_by', 'created_at_formatted', 'created_at', 'attachments', 'post_to',) 

class SharePostSerializer(serializers.ModelSerializer):
    created_by = UserLessSerializer(read_only=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    post_to = UserLessSerializer(read_only=True)
    post = PostLessSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'body', 'post', 'is_private','only_me', 'created_by', 'likes_count', 'comments_count', 'created_at_formatted', 'created_at', 'attachments', 'post_to',)

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
    group = GroupSerializer(read_only=True)
    class Meta:
        model = GroupPost
        fields = ('id', 'body', 'group', 'likes_count', 'comments_count', 'comments', 'created_by', 'created_at_formatted', 'created_at', 'attachments', 'likes','is_anonymous', 'pending',)  
        
class AnonymousGroupPostSerializer(serializers.ModelSerializer):
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    likes = MemberLikeSerializer(read_only=True, many=True)
    comments = MemberCommentSerializer(read_only=True, many=True)
    class Meta:
        model = GroupPost
        fields = ('id', 'body', 'likes_count', 'comments_count', 'comments', 'created_at_formatted', 'created_at', 'attachments', 'likes', 'is_anonymous',)  
        
class GroupPostPollSerializer(serializers.ModelSerializer):
    created_by = MemberSerializer(read_only=True)
    options = PollOptionSerializer(read_only=True, many=True)
    class Meta:
        model = GroupPostPoll
        fields = ('id', 'body', 'created_by', 'created_at_formatted', 'created_at', 'allow_add_option', 'multiple_options', 'options','is_anonymous', 'pending',)  
        
class AnonymousGroupPostPollSerializer(serializers.ModelSerializer):
    options = PollOptionSerializer(read_only=True, many=True)
    class Meta:
        model = GroupPostPoll
        fields = ('id', 'body', 'created_at_formatted', 'created_at', 'options', 'is_anonymous', 'allow_add_option', 'multiple_options',)  
        
class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    likes = LikeSerializer(read_only=True, many=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    page_likes = PageLikeSerializer(read_only=True, many=True)
    page_comments = PageCommentSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ('id', 'body', 'likes_count', 'likes','comments_count', 'created_by','is_private','only_me', 'created_at_formatted','comments','attachments','page_likes','page_comments', 'is_avatar_post',)
        
class SharePostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    likes = LikeSerializer(read_only=True, many=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    page_likes = PageLikeSerializer(read_only=True, many=True)
    page_comments = PageCommentSerializer(read_only=True, many=True)
    post = PostLessSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'body', 'post', 'likes_count', 'likes','comments_count', 'created_by','is_private','only_me', 'created_at_formatted','comments','attachments','page_likes','page_comments', 'post_to',)
        
class PagePostDetailSerializer(serializers.ModelSerializer):
    created_by = PageSerializer(read_only=True)
    comments = PageCommentSerializer(read_only=True, many=True)
    likes = PageLikeSerializer(read_only=True, many=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    page_likes = PageLikeSerializer(read_only=True, many=True)
    page_comments = PageCommentSerializer(read_only=True, many=True)
    class Meta:
        model = PagePost
        fields = ('id', 'body', 'likes_count', 'likes','comments_count', 'created_by', 'created_at_formatted','comments','attachments','page_likes','page_comments','is_avatar_post',)

class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ('id', 'hashtag', 'occurences',)