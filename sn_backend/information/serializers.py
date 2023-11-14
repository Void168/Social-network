from rest_framework import serializers

from account.serializers import UserSerializer

from .models import Website, PhoneNumber

class WebsiteSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Website
        fields = ('id', 'created_by', 'url','is_private','only_me')
class PhoneNumberSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = PhoneNumber
        fields = ('id','created_by', 'phone_number','is_private','only_me',)