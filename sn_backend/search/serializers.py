from rest_framework import serializers

from .models import SearchKeyWord, GroupSearchKeyWord
from account.serializers import UserLessSerializer
from group.serializers import MemberSerializer 

class GroupSearchKeyWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupSearchKeyWord
        fields = ('id', 'body',)
        
class SearchKeyWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchKeyWord
        fields = ('id', 'body',)