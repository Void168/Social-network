from rest_framework import serializers

from .models import Group, Rule, Question
from account.serializers import UserSerializer

class QuestionSerializer(serializers.ModelSerializer):
    model = Question
    fields = ('body',)

class RuleSerializer(serializers.ModelSerializer):
    model = Rule
    fields = ('name','body',)

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        members = UserSerializer(read_only=True, many=True)
        admin = UserSerializer(read_only=True)
        moderators = UserSerializer(read_only=True, many=True)
        rules = RuleSerializer(read_only=True, many=True)
        questions = QuestionSerializer(read_only=True, many=True)
        fields = ('id', 'name', 'email', 'members','members_count','get_avatar','get_cover_image', 'created_at','admin','moderators', 'biography', 'is_private_group', 'today_posts_count', 'rules','questions',)