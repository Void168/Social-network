from django.db.models import Q
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from account.serializers import UserSerializer

from notification.utils import create_notification

# from .forms import
from .models import TextStory, MediaStory, ReactStory, StoryAttachment
from .serializers import StoryAttachmentSerializer, ReactStorySerializer, TextStorySerializer, MediaStorySerializer, TextStoryDetailSerializer, MediaStoryDetailSerializer

from notification.serializers import NotificationSerializer

@api_view(['GET'])
def text_story_list(request):
    user_ids = [request.user.id]
    current_user = request.user
    friends = User.objects.get(Q(email=current_user)).friends.all()
    
    for user in request.user.friends.all():
        user_ids.append(user.id)
            
    text_stories = TextStory.objects.filter(Q(created_by__in=list(user_ids), only_me=False) | Q(post_to__in=list(friends), only_me=False))
    
    serializer = TextStorySerializer(text_stories, many=True)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def media_story_list(request):
    user_ids = [request.user.id]
    current_user = request.user
    friends = User.objects.get(Q(email=current_user)).friends.all()
    
    for user in request.user.friends.all():
        user_ids.append(user.id)
            
    media_stories = MediaStory.objects.filter(Q(created_by__in=list(user_ids), only_me=False) | Q(post_to__in=list(friends), only_me=False))
    
    serializer = MediaStorySerializer(media_stories, many=True)
    
    return JsonResponse(serializer.data, safe=False)

