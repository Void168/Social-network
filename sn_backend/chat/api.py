from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.db.models import Q

from .forms import MessageForm, AttachmentForm, ChooseThemeForm

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
def conversation_get(request, pk):

    conversation = Conversation.objects.get(pk=pk)

    serializer = ConversationDetailSerializer(conversation)
    
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

@api_view(['DELETE'])
def conversation_delete(request, pk):
    conversation = Conversation.objects.get(pk=pk)
    conversation.delete()
    
    return JsonResponse({'message': 'conversation deleted'})
    
