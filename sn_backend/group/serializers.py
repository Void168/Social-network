from rest_framework import serializers

from .models import Group, Rule, Question, Member, PageMember, JoinGroupRequest, Question, Answer
from account.serializers import UserSerializer, UserLessSerializer
from page.serializers import PageSerializer 

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('body',)

class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ('name','body',)

class MemberSerializer(serializers.ModelSerializer):
    information = UserLessSerializer(read_only=True)
    class Meta:
        model = Member
        fields = ('id','information','date_join_group','last_access', 'last_access_formatted',)
    
class PageMemberSerializer(serializers.ModelSerializer):
    model = PageMember
    class Meta:
        information = PageSerializer(read_only=True)
        fields = ('id','information','date_join_group','last_access',)
    
class GroupSerializer(serializers.ModelSerializer):
    admin = UserLessSerializer(read_only=True)
    moderators = UserLessSerializer(read_only=True, many=True)
    
    class Meta:
        model = Group
        fields = ('id', 'name', 'members_count','get_cover_image', 'created_at','admin','moderators', 'biography', 'is_private_group', 'show_group', 'today_posts_count', 'created_at_formatted',)
        
class GroupDetailSerializer(serializers.ModelSerializer):
    members = MemberSerializer(read_only=True, many=True)
    page_members = PageMemberSerializer(read_only=True, many=True)
    admin = UserLessSerializer(read_only=True)
    moderators = MemberSerializer(read_only=True, many=True)
    rules = RuleSerializer(read_only=True, many=True)
    questions = QuestionSerializer(read_only=True, many=True)
    
    class Meta:
        model = Group
        fields = ('id', 'name', 'email', 'website', 'members', 'page_members', 'members_count','get_cover_image', 'created_at','admin','moderators', 'biography', 'is_private_group', 'show_group', 'anyone_can_join', 'anonymous_post', 'anyone_can_post', 'pending_post', 'anyone_can_poll', 'today_posts_count', 'rules','questions', 'created_at_formatted',)



class QuestionSerializer(serializers.ModelSerializer):
    created_by = GroupSerializer(read_only=True)
    class Meta:
        model = Question
        fields = ('id', 'body', 'created_by',)
        
class AnswerSerializer(serializers.ModelSerializer):
    created_by = GroupSerializer(read_only=True)
    question = QuestionSerializer(read_only=True)
    class Meta:
        model = Question
        fields = ('id', 'body', 'created_by', 'question',)

class JoinGroupRequestSerializer(serializers.ModelSerializer):
    created_by = UserLessSerializer(read_only=True)
    created_for = GroupSerializer(read_only=True)
    answers = AnswerSerializer(read_only=True, many=True)
    class Meta:
        model = JoinGroupRequest
        fields = ('id', 'created_by', 'created_for', 'created_at','status', 'created_at_formatted', 'answers',)