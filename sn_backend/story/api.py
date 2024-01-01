from django.db.models import Q
from django.http import JsonResponse
from datetime import datetime, timedelta

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from account.serializers import UserSerializer
from .forms import TextStoryForm, MediaStoryForm, StoryAttachmentForm

from notification.utils import create_notification

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
    
    text_stories = TextStory.objects.filter(Q(created_by__in=list(user_ids), only_me=False))
    now = datetime.now()
    
    for text_story in text_stories:
        if (now - timedelta(hours=24)).timestamp() > (text_story.created_at).timestamp():
            text_story.delete()
            
    serializer = TextStorySerializer(text_stories, many=True)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def user_text_story_list(request, id):
    user = User.objects.get(pk=id)
    text_stories = TextStory.objects.filter(created_by_id=id)

    if not request.user in user.friends.all():
        text_stories = text_stories.filter(Q(is_private=False) & Q(only_me=False))
    
    if request.user in user.friends.all():
        text_stories = text_stories.filter(only_me=False)
        
    if request.user == user:
        text_stories = TextStory.objects.filter(created_by_id=id)
    
    text_stories.order_by('-created_at')
        
    text_stories_serializer = TextStoryDetailSerializer(text_stories, many=True)

    return JsonResponse({
        'stories': text_stories_serializer.data,
    }, safe=False)
    
@api_view(['GET'])
def media_story_list(request):
    user_ids = [request.user.id]
    current_user = request.user
    friends = User.objects.get(Q(email=current_user)).friends.all()
    
    for user in request.user.friends.all():
        user_ids.append(user.id)
            
    media_stories = MediaStory.objects.filter(Q(created_by__in=list(user_ids), only_me=False))
    
    now = datetime.now()
    
    for media_story in media_stories:
        if (now - timedelta(hours=24)).timestamp() > (media_story.created_at).timestamp():
            media_story.delete()
    
    serializer = MediaStorySerializer(media_stories, many=True)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def user_media_story_list(request, id):
    user = User.objects.get(pk=id)
    media_stories = MediaStory.objects.filter(created_by_id=id)

    if not request.user in user.friends.all():
        media_stories = media_stories.filter(Q(is_private=False) & Q(only_me=False))
    
    if request.user in user.friends.all():
        media_stories = media_stories.filter(only_me=False)
        
    if request.user == user:
        media_stories = MediaStory.objects.filter(created_by_id=id)
    
    media_stories.order_by('-created_at')
        
    media_stories_serializer = MediaStoryDetailSerializer(media_stories, many=True)

    return JsonResponse({
        'stories': media_stories_serializer.data,
    }, safe=False)

@api_view(['POST'])
def create_text_story(request):
    form = TextStoryForm(request.POST)

    if form.is_valid():
        text_story = form.save(commit=False)
        text_story.created_by = request.user
        text_story.save()

        serializer = TextStorySerializer(text_story)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add something here later!...'})

@api_view(['POST'])
def create_media_story(request):
    form = MediaStoryForm(request.POST)
    attachment = None
    story_attachment_form = StoryAttachmentForm(request.POST, request.FILES)

    if story_attachment_form.is_valid():
        attachment = story_attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()
        
    if form.is_valid():
        media_story = form.save(commit=False)
        media_story.created_by = request.user
        media_story.save()

        if attachment:
            media_story.attachments.add(attachment)

        serializer = MediaStorySerializer(media_story)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add something here later!...'})

@api_view(['POST'])
def seen_text_story(request, pk):
    text_story = TextStory.objects.get(pk=pk)
    seenUser = request.user
    
    if not text_story.seen_by.all().filter(created_by=request.user) and text_story.created_by == seenUser:
        text_story.seen_by.add(seenUser)
        text_story.save()
    
        serializer = TextStoryDetailSerializer(text_story)
            
        return JsonResponse({'message': serializer.data})
    else:
        return JsonResponse({'message': 'conversation not exists'})

@api_view(['DELETE'])
def text_story_delete(request, pk):
    text_story = TextStory.objects.filter(created_by=request.user).get(pk=pk)
    text_story.delete()
    
    return JsonResponse({'message': 'text story deleted'})

@api_view(['DELETE'])
def text_media_delete(request, pk):
    media_story = MediaStory.objects.filter(created_by=request.user).get(pk=pk)
    media_story.delete()
    
    return JsonResponse({'message': 'text media deleted'})
