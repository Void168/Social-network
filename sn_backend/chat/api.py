from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.db.models import Q

from .forms import MessageForm, GroupMessageForm, AttachmentForm, ChooseThemeForm

from account.models import User
from .models import Conversation, GroupConversation, ConversationMessage, SeenUser
from .serializers import ConversationSerializer, ConversationDetailSerializer, GroupConversationSerializer, ConversationMessageSerializer, GroupConversationMessageSerializer, SeenUserSerializer

@api_view(['GET'])
def conversation_list(request):
    conversations = Conversation.objects.filter(users__in=list([request.user]))
    
    serializer = ConversationSerializer(conversations, many=True)
        
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def group_conversation_list(request):
    group_conversations = GroupConversation.objects.filter(users__in=list([request.user]))
    
    serializer = GroupConversationSerializer(group_conversations, many=True)
        
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def conversation_detail(request, pk):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    serializer = ConversationDetailSerializer(conversation)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def group_conversation_detail(request, pk):
    group_conversation = GroupConversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    serializer = GroupConversationSerializer(group_conversation)
    
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

    conversation = Conversation.objects.create()
    conversation.users.add(user, request.user)
    conversation.save()

    serializer = ConversationDetailSerializer(conversation)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def conversation_get(request, pk):

    conversation = Conversation.objects.get(pk=pk)

    serializer = ConversationDetailSerializer(conversation)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def group_conversation_create(request):
    users = request.data.get('users')
    group_chat = GroupConversation.objects.create(admin=request.user)
    group_chat.users.add(request.user)
    
    for user in users:
        group_chat.users.add(user)
        
    group_chat.save()

    serializer = GroupConversationSerializer(group_chat)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def group_conversation_get(request, pk):

    group_conversation = GroupConversation.objects.get(pk=pk)

    serializer = GroupConversationSerializer(group_conversation)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def conversation_send_message(request, pk):
    form = MessageForm(request.POST)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)
    
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    seenUser = SeenUser.objects.create(created_by=request.user)
    
    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if form.is_valid():
        message = form.save(commit=False)
        message.created_by = request.user
        message.conversation = conversation
        for user in conversation.users.all():
            if user != request.user:
                sent_to = user
                message.sent_to = sent_to
                
        message.save()
        
        if attachment:
            message.attachments.add(attachment)
            message.save()
        
        message.seen_by.add(seenUser)
        message.save()

        serializer = ConversationMessageSerializer(message)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add something here later!...'})

@api_view(['POST'])
def group_conversation_send_message(request, pk):
    form = GroupMessageForm(request.POST)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)
    
    group_conversation = GroupConversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    seenUser = SeenUser.objects.create(created_by=request.user)
    
    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if form.is_valid():
        group_message = form.save(commit=False)
        group_message.created_by = request.user
        group_message.group_conversation = group_conversation
        for user in group_conversation.users.all():
            if user != request.user:
                sent_to = user
                group_message.sent_to = sent_to
                
        group_message.save()
        
        if attachment:
            group_message.attachments.add(attachment)
            group_message.save()
        
        group_message.seen_by.add(seenUser)
        group_message.save()

        serializer = GroupConversationMessageSerializer(group_message)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add something here later!...'})

@api_view(['POST'])
def choose_theme(request, pk):
    current_user = request.user
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    form = ChooseThemeForm(data=request.POST, instance=current_user)
    
    if form.is_valid():
        form.save()
        conversation.theme = request.POST['theme']
        conversation.save()
    
        serializer = ConversationDetailSerializer(conversation)
    
        return JsonResponse(serializer.data)
    else: 
        return JsonResponse({'message':'Failed'})
    

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

@api_view(['POST'])
def group_set_seen(request, pk):
    group_conversation = GroupConversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    seenUser = SeenUser.objects.create(created_by=request.user)
        
    group_messages = group_conversation.group_messages.exclude(created_by=request.user)
    
    for group_message in group_messages:
        if not group_message.seen_by.all().filter(created_by=request.user):
            group_message.seen_by.add(seenUser)
            group_message.save()
            
    return JsonResponse({'group_message': 'Seen'})

@api_view(['DELETE'])
def conversation_delete(request, pk):
    conversation = Conversation.objects.get(pk=pk)
    conversation.delete()
    
    return JsonResponse({'message': 'conversation deleted'})
    
