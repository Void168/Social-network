from django.db.models import Q
from django.http import JsonResponse
from datetime import datetime, timedelta

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from account.serializers import UserSerializer
from .forms import TextStoryForm, MediaStoryForm, StoryAttachmentForm

from notification.utils import create_notification

from notification.models import Notification
from .models import TextStory, MediaStory, ReactStory, StoryAttachment
from .serializers import StoryAttachmentSerializer, ReactStorySerializer, TextStorySerializer, MediaStorySerializer, TextStoryDetailSerializer, MediaStoryDetailSerializer

from notification.serializers import NotificationSerializer

@api_view(['GET'])
def text_story_list(request):
    user_ids = [request.user.id]
    current_user = request.user
    friends = User.objects.get(Q(email=current_user)).friends.all()
    following = User.objects.get(Q(email=current_user)).following.all()
    
    for user in request.user.friends.all():
        user_ids.append(user.id)
    
    text_stories = TextStory.objects.filter(Q(created_by__in=list(user_ids), only_me=False) | Q(created_by__in=list(following), only_me=False, is_private=False))
    
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
    following = User.objects.get(Q(email=current_user)).following.all()
    
    for user in request.user.friends.all():
        user_ids.append(user.id)
            
    media_stories = MediaStory.objects.filter(Q(created_by__in=list(user_ids), only_me=False) | Q(created_by__in=list(following), only_me=False, is_private=False))
    
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

@api_view(['GET'])
def get_detail_text_story(request, pk):
    if pk in list(TextStory.objects.all().values_list('id', flat=True)):
        text_story = TextStory.objects.get(pk=pk)
        
        serializer = TextStoryDetailSerializer(text_story)
    
        return JsonResponse(serializer.data)
    else:
        return JsonResponse({'message': 'No text story found'})

@api_view(['GET'])
def get_detail_media_story(request, pk):
    if pk in list(MediaStory.objects.all().values_list('id', flat=True)):
        media_story = MediaStory.objects.get(pk=pk)
    
        serializer = MediaStoryDetailSerializer(media_story)
    
        return JsonResponse(serializer.data)
    else:
        return JsonResponse({'message': 'No media story found'})

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
    
    if not text_story.seen_by.all().filter(id=request.user.id) and text_story.created_by != seenUser:
        text_story.seen_by.add(seenUser)
        text_story.save()
    
        serializer = TextStoryDetailSerializer(text_story)
            
        return JsonResponse(serializer.data)
    else:
        return JsonResponse({'message': 'seen'})
    
@api_view(['POST'])
def seen_media_story(request, pk):
    media_story = MediaStory.objects.get(pk=pk)
    seenUser = request.user
    
    if not media_story.seen_by.all().filter(id=request.user.id) and media_story.created_by != seenUser:
        media_story.seen_by.add(seenUser)
        media_story.save()
    
        serializer = MediaStoryDetailSerializer(media_story)
            
        return JsonResponse(serializer.data)
    else:
        return JsonResponse({'message': 'seen'})
    
@api_view(['POST'])
def react_text_story(request, pk, status):
    text_story = TextStory.objects.get(pk=pk)
    react_story = ReactStory.objects.create(created_by=request.user)
    
    if(status == 'like'):
        react_story.type_of_react = "👍"
    elif(status == 'heart'):
        react_story.type_of_react = "❤️"
    elif(status == 'love'):
        react_story.type_of_react = "😍"
    elif(status == 'laugh'):
        react_story.type_of_react = "😆"
    elif(status == 'suprise'):
        react_story.type_of_react = "😲"
    elif(status == 'sad'):
        react_story.type_of_react = "😥"
    elif(status == 'angry'):
        react_story.type_of_react = "😡"
        
    react_story.save()

    received_user = text_story.created_by
    
    if not text_story.reacted_by.filter(created_by=request.user):
        text_story.reacted_by.add(react_story)
        text_story.save()
        
        notification = Notification.objects.create(
            body=f'{received_user.name} đã thả {react_story.type_of_react} vào tin của bạn',
            type_of_notification='react_story',
            created_by=request.user,
            created_for=received_user
        )
        
        serializer_notification = NotificationSerializer(notification)
        
        serializer = ReactStorySerializer(react_story)
        
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'message': 'story already reacted'})

@api_view(['POST'])
def react_media_story(request, pk, status):
    media_story = MediaStory.objects.get(pk=pk)
    react_story = ReactStory.objects.create(created_by=request.user)
    
    if(status == 'like'):
        react_story.type_of_react = "👍"
    elif(status == 'heart'):
        react_story.type_of_react = "❤️"
    elif(status == 'love'):
        react_story.type_of_react = "😍"
    elif(status == 'laugh'):
        react_story.type_of_react = "😆"
    elif(status == 'suprise'):
        react_story.type_of_react = "😲"
    elif(status == 'sad'):
        react_story.type_of_react = "😥"
    elif(status == 'angry'):
        react_story.type_of_react = "😡"
        
    react_story.save()

    received_user = media_story.created_by
    
    if not media_story.reacted_by.filter(created_by=request.user):
        media_story.reacted_by.add(react_story)
        media_story.save()
        
        notification = Notification.objects.create(
            body=f'{received_user.name} đã thả {react_story.type_of_react} vào tin của bạn',
            type_of_notification='react_story',
            created_by=request.user,
            created_for=received_user
        )
        
        serializer_notification = NotificationSerializer(notification)
        
        serializer = ReactStorySerializer(react_story)
        
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'message': 'story already reacted'})
    
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
