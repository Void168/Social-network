from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.db.models import Q

from account.models import User
from .models import Conversation, ConversationMessage, SeenUser
from .serializers import ConversationSerializer, ConversationDetailSerializer, ConversationMessageSerializer, SeenUserSerializer

@api_view(['GET'])
def conversation_list(request):
    conversations = Conversation.objects.filter(users__in=list([request.user]))
    
    serializer = ConversationSerializer(conversations, many=True)
        
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def conversation_detail(request, pk):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    serializer = ConversationDetailSerializer(conversation)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def conversation_get_or_create(request, user_pk):
    user = User.objects.get(pk=user_pk)

    conversations = Conversation.objects.filter(users__in=list([request.user])).filter(users__in=list([user]))

    if conversations.exists():
        conversation = conversations.first()
    else:
        conversation = Conversation.objects.create()
        conversation.users.add(user, request.user)
        conversation.save()

    serializer = ConversationDetailSerializer(conversation)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def conversation_create(request, user_pk):
    user = User.objects.get(pk=user_pk)

    conversations = Conversation.objects.filter(users__in=list([request.user])).filter(users__in=list([user]))

    conversation = Conversation.objects.create()
    conversation.users.add(user, request.user)
    conversation.save()

    serializer = ConversationDetailSerializer(conversation)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def conversation_get(request, user_pk):
    user = User.objects.get(pk=user_pk)

    conversations = Conversation.objects.filter(users__in=list([request.user])).filter(users__in=list([user]))

    conversation = conversations.first()

    serializer = ConversationDetailSerializer(conversation)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def conversation_send_message(request, pk):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    seenUser = SeenUser.objects.create(created_by=request.user)
    
    for user in conversation.users.all():
        if user != request.user:
            sent_to = user

    conversation_message = ConversationMessage.objects.create(
        conversation=conversation,
        body=request.data.get('body'),
        created_by=request.user,
        sent_to=sent_to,
    )
    
    conversation_message.seen_by.add(seenUser)

    serializer = ConversationMessageSerializer(conversation_message)

    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def set_seen(request, pk):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    seenUser = SeenUser.objects.create(created_by=request.user)
        
    messages = conversation.messages.exclude(created_by=request.user)
    
    for message in messages:
        if not message.seen_by.all().filter(created_by=request.user):
            message.seen_by.add(seenUser)
            message.save()
            
    return JsonResponse({'message': 'Seen'})

@api_view(['DELETE'])
def conversation_delete(request, pk):
    conversation = Conversation.objects.get(pk=pk)
    conversation.delete()
    
    return JsonResponse({'message': 'conversation deleted'})
    
