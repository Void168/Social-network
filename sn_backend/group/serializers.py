from rest_framework import serializers

from .models import Group, Rule, Question, Member, PageMember
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
        fields = ('id','information','date_join_group','last_access',)
    
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
    moderators = UserLessSerializer(read_only=True, many=True)
    rules = RuleSerializer(read_only=True, many=True)
    questions = QuestionSerializer(read_only=True, many=True)
    
    class Meta:
        model = Group
        fields = ('id', 'name', 'email', 'members', 'page_members', 'members_count','get_cover_image', 'created_at','admin','moderators', 'biography', 'is_private_group', 'show_group', 'today_posts_count', 'rules','questions', 'created_at_formatted',)