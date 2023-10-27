from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from .models import Conversation, ConversationMessage
from .serializers import ConversationSerializer, ConversationDetailSerializer, ConversationMessageSerializer, LastMessageSerializer

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
def conversation_send_message(request, pk):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)

    for user in conversation.users.all():
        if user != request.user:
            sent_to = user

    conversation_message = ConversationMessage.objects.create(
        conversation=conversation,
        body=request.data.get('body'),
        created_by=request.user,
        sent_to=sent_to
    )

    serializer = ConversationMessageSerializer(conversation_message)

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def get_last_message(request, pk):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    last_message = conversation.messages.order_by('-created_at')[0]
    if last_message:
        last_message.is_latest_message=True
        
    serializer = LastMessageSerializer(last_message)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def set_seen(request, pk):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    message = conversation.messages.order_by('-created_at')[0]
    current_user = request.user
    if message.sent_to.id == current_user.id and conversation.seen == False:
        conversation.seen = True
        conversation.save()
        
        return JsonResponse({'message': 'Seen'})
    else:
        return JsonResponse({'message': 'Unseen'})

# @api_view(['POST'])
# def set_unseen(request, pk):
#     conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)
#     message = conversation.messages.order_by('-created_at')[0]
#     current_user = request.user
    
#     if message.created_by.id != current_user.id and conversation.seen == True:
#         conversation.seen = False
#         conversation.save()
        
#         return JsonResponse({'message': 'Unseen'})
    
#     else:
#         return JsonResponse({'message': 'Seen'})
