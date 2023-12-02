from django.http import JsonResponse
from datetime import datetime
from .pusher import pusher_client
from django.core import serializers
import json

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.db.models import Q

from .forms import MessageForm, GroupMessageForm, AttachmentForm, ChooseThemeForm, ChooseGroupThemeForm, ChangeGroupNameForm, AvatarGroupForm

from account.models import User
from .models import Conversation, GroupConversation, ConversationMessage, SeenUser, GroupPoll, PollOption, GroupNotification
from .serializers import ConversationSerializer, ConversationDetailSerializer, GroupConversationSerializer, ConversationMessageSerializer, GroupConversationMessageSerializer, SeenUserSerializer, GroupPollSerializer, GroupNotificationSerializer

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
def chat_window_detail(request, user_pk):
    friend = User.objects.get(pk=user_pk)
    conversation = Conversation.objects.filter(users__in=list([request.user])).filter(users__in=list([friend]))
    
    if conversation.count():
        main_conversation = conversation[0]
        serializer = ConversationSerializer(main_conversation)
    
        return JsonResponse({'message':'Success', 'conversation': serializer.data})
    else:
        return JsonResponse({'message':'Conversation not exists'})

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
    user1 = User.objects.get(id=users[0])
    group_chat = GroupConversation.objects.create(admin=request.user)
    group_chat.group_name = f'Đoạn chat nhóm giữa {request.user.name}, {user1.name} và {(len(users) - 1)} người khác nữa'
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
    
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(id=pk)
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
        
        serializer_data = serializer.data
        json_data = json.dumps(serializer_data)
        
        pusher_client.trigger(str(pk), 'message:new', {'message': json_data})
    

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
        
        serializer_data = serializer.data
        json_data = json.dumps(serializer_data)
        
        pusher_client.trigger(str(pk), 'group_message:new', {'message': json_data})

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add something here later!...'})

@api_view(['GET'])
def get_group_notifications(request, pk):
    group_conversation = GroupConversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    notifications = GroupNotification.objects.filter(Q(group_conversation=group_conversation))
    
    serializer = GroupNotificationSerializer(notifications, many=True)
    
    return JsonResponse(serializer.data, safe=False)
    
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
def choose_group_theme(request, pk):
    current_user = request.user
    group_conversation = GroupConversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    form = ChooseGroupThemeForm(data=request.POST, instance=current_user)
    
    if form.is_valid():
        form.save()
        group_conversation.theme = request.POST['theme']
        group_conversation.save()
        content = f'{current_user.name} đã thay đổi chủ đề thành {group_conversation.theme}'
        theme_notification = GroupNotification.objects.create(group_conversation=group_conversation,content=content)
    
        serializer = GroupConversationSerializer(group_conversation)
        serializer1 = GroupNotificationSerializer(theme_notification)
    
        return JsonResponse({'group':serializer.data, 'notification':serializer1.data})
    else: 
        return JsonResponse({'message':'Failed'})

@api_view(['POST'])
def set_group_avatar(request, pk):
    current_user = request.user
    group_conversation = GroupConversation.objects.filter(users__in=list([request.user])).get(pk=pk)

    form = AvatarGroupForm(request.FILES, instance=user)
    if form.is_valid():
        form.save()
        group_conversation.avatar = request.FILES['avatar']
        content = f'{current_user.name} đã thay đổi ảnh nhóm'
        theme_notification = GroupNotification.objects.create(group_conversation=group_conversation,content=content)
        group_conversation.save()
    
    serializer = GroupConversationSerializer(group_conversation)
    
    return JsonResponse({'message': 'avatar updated'})

@api_view(['POST'])
def set_group_name(request, pk):
    current_user = request.user
    group_conversation = GroupConversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    form = ChangeGroupNameForm(data=request.POST, instance=current_user)
    
    if form.is_valid():
        form.save()
        group_conversation.group_name = request.POST['group_name']
        content = f'{current_user.name} đã thay đổi tên nhóm thành {group_conversation.group_name}'
        theme_notification = GroupNotification.objects.create(group_conversation=group_conversation,content=content)
        group_conversation.save()
    
        serializer = GroupConversationSerializer(current_user)
    
        return JsonResponse(serializer.data)
    else: 
        return JsonResponse({'message':'Failed'})

@api_view(['POST'])
def add_users(request, pk):
    other_user_id =request.data.get('otherUser')
    
    users = request.data.get('users')
    group_conversation = GroupConversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    for user in users:
        group_conversation.users.add(user)
    
    if other_user_id != "":
        other_user = User.objects.get(id=other_user_id)
    
        group_conversation.users.add(other_user)
    
    group_conversation.save()
    
    serializer = GroupConversationSerializer(group_conversation)
    
    return JsonResponse({'message':'users update', 'group_conversation': serializer.data})

@api_view(['POST'])
def set_moderator(request, pk, user_pk):
    user = User.objects.get(pk=user_pk)
    group_conversation = GroupConversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    
    group_conversation.moderators.add(user)
        
    group_conversation.save()
    
    serializer = GroupConversationSerializer(group_conversation)
    
    return JsonResponse({'message':'Successful'})

@api_view(['POST'])
def create_poll(request, pk):
    group_conversation = GroupConversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    time_end = request.data.get('time_end')
    poll_name = request.data.get('poll_name')
    
    poll = GroupPoll.objects.create(
        created_by=request.user,
        group_conversation=group_conversation, 
        poll_name=poll_name, 
        time_end=time_end
    )
    
    list_poll_options = request.data.get('options')
    list_options = [sub['name'] for sub in list_poll_options]
    for option in list_options:
        poll_option = PollOption.objects.create(poll_option_name=option)
        poll.poll_options.add(poll_option)
        
    content = f'{request.user.name} đã tạo cuộc thảo luận {poll_name}'
    theme_notification = GroupNotification.objects.create(group_conversation=group_conversation,content=content)
    
    poll.save()
    
    serializer = GroupPollSerializer(poll)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def group_polls_list(request, pk):
    group_conversation = GroupConversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    list_polls = GroupPoll.objects.filter(Q(group_conversation=group_conversation))
    
    serializer = GroupPollSerializer(list_polls, many=True)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def vote_poll(request, pk, conversation_pk):
    group_conversation = GroupConversation.objects.filter(users__in=list([request.user])).get(pk=conversation_pk)
    poll_option = PollOption.objects.get(pk=pk)
    if poll_option.users_vote.all().filter(id=request.user.id).exists():
        poll_option.users_vote.remove(request.user)
        poll_option.save()
    else: 
        poll_option.users_vote.add(request.user)
        content = f'{request.user.name} đã bình chọn {poll_option.poll_option_name}'
        theme_notification = GroupNotification.objects.create(group_conversation=group_conversation,content=content)
        poll_option.save()
        
    return JsonResponse({'message': 'Success'})

@api_view(['DELETE'])
def delete_poll(request, pk):
    poll = GroupPoll.objects.get(pk=pk)
    if poll.created_by == request.user:
        poll.delete()
        
    return JsonResponse({'message': 'Success'})
    

@api_view(['POST'])
def kick_user(request, pk, user_pk):
    user_wanna_kick = User.objects.get(pk=user_pk)
    group_conversation = GroupConversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    list_moderators = []
    for moderator in group_conversation.moderators.all():
        list_moderators.append(moderator)
    
    if group_conversation.admin == request.user or request.user in list_moderators:
        group_conversation.users.remove(user_wanna_kick)
        
    group_conversation.save()
    
    serializer = GroupConversationSerializer(group_conversation)
    
    return JsonResponse({'message':'kick user successfully'})

@api_view(['POST'])
def leave_group(request, pk, user_pk):
    leave_user = User.objects.get(pk=user_pk)
    group_conversation = GroupConversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    admin = group_conversation.admin
    if leave_user == admin and group_conversation.moderators.count():
        group_conversation.admin = group_conversation.moderators.all()[0]
        group_conversation.moderators.remove(group_conversation.admin)
        
    else:
        group_conversation.admin = group_conversation.users.all()[0]
        
    group_conversation.users.remove(leave_user)     
    group_conversation.save()
    
    serializer = GroupConversationSerializer(group_conversation)
    
    return JsonResponse({'message':'Left group', 'group_conversation': serializer.data})

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

@api_view(['DELETE'])
def group_conversation_delete(request, pk):
    group_conversation = GroupConversation.objects.get(pk=pk)
    group_conversation.delete()
    
    return JsonResponse({'message': 'group conversation deleted'})
    
