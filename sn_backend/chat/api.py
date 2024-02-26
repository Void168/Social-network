from django.http import JsonResponse
import sys
from datetime import datetime
from .pusher import pusher_client
import json
from django.core import serializers
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.db.models import Q

from .forms import MessageForm, GroupMessageForm, AttachmentForm, ChooseThemeForm, ChooseGroupThemeForm, ChangeGroupNameForm, AvatarGroupForm, PageMessageForm, PageAttachmentForm

from account.models import User
from page.models import Page
from .models import Conversation, GroupConversation, ConversationMessage, SeenUser, GroupPoll, PollOption, GroupNotification, PageConversation, SeenPage
from .serializers import ConversationSerializer, ConversationDetailSerializer, GroupConversationSerializer, ConversationMessageSerializer, GroupConversationMessageSerializer, SeenUserSerializer, GroupPollSerializer, GroupNotificationSerializer, PageConversationSerializer, PageConversationMessageSerializer

@api_view(['GET'])
def conversation_list(request):
    conversations = Conversation.objects.filter(users__in=list([request.user]))
    page_conversations = PageConversation.objects.filter(user=request.user)
    
    serializer = ConversationSerializer(conversations, many=True)
    page_serializer = PageConversationSerializer(page_conversations, many=True)
        
    return JsonResponse({
        'conversations': serializer.data,
        'page_conversations': page_serializer.data
        }, safe=False)

@api_view(['GET'])
def page_conversation_list(request, id):
    current_page = Page.objects.get(id=id)
    page_conversations = PageConversation.objects.filter(page=current_page)
    
    serializer = PageConversationSerializer(page_conversations, many=True)
        
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
def page_conversation_detail(request, pk):
    page_conversation = PageConversation.objects.get(pk=pk)
    serializer = PageConversationSerializer(page_conversation)
        
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
def page_conversation_get_or_create(request, user_pk, id):
    current_page = Page.objects.get(id=id)
    user = User.objects.get(pk=user_pk)

    page_conversations = PageConversation.objects.filter(user=user).filter(page=current_page)
    
    if page_conversations.exists():
        page_conversation = page_conversations.first()
    else:
        page_conversation = PageConversation.objects.create(
            user = user,
            page = current_page
        )

        page_conversation.save()

        serializer = PageConversationSerializer(page_conversation)
    
        return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def conversation_get(request, pk):

    conversation = Conversation.objects.get(pk=pk)

    serializer = ConversationDetailSerializer(conversation)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def page_conversation_get(request, pk):

    page_conversation = PageConversation.objects.get(pk=pk)

    serializer = PageConversationSerializer(conversation)
    
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

@authentication_classes([TokenAuthentication,SessionAuthentication, BasicAuthentication,])
@permission_classes([IsAuthenticated,])
@api_view(['POST'])
def pusher_auth(request, pk):
    conversation = Conversation.objects.filter(users__in=list([request.user])).get(pk=pk)
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    if not request.user.is_member_of_team(f'presence-{str(pk)}'):
        return HttpResponseForbidden()

    payload = pusher_client.authenticate(
        channel=request.POST['channel_name'],
        socket_id=request.POST['socket_id'],
        custom_data={
            'user_id': request.user.id,
            'user_info': {
                'username': request.user.name,
                'useremail': request.user.email,
            }
        }
    )
        
    return JsonResponse(payload)

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
        
        pusher_client.trigger(f'{str(pk)}', 'message:new', {'message': json_data})
        
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add something here later!...'})
    
@api_view(['POST'])
def page_conversation_send_message(request, pk, id):
    page = Page.objects.get(id=id)
    form = PageMessageForm(request.POST)
    page_attachment = None
    page_attachment_form = PageAttachmentForm(request.POST, request.FILES)
    
    page_conversation = PageConversation.objects.filter(page=page).get(id=pk)
    seenPage = SeenPage.objects.create(created_by=page)
    
    if page_attachment_form.is_valid():
        page_attachment = page_attachment_form.save(commit=False)
        page_attachment.created_by = page
        page_attachment.save()

    if form.is_valid():
        page_message = form.save(commit=False)
        page_message.created_by_page = page
        page_message.conversation = page_conversation

        sent_to = page_conversation.user
        page_message.sent_to = sent_to
                
        page_message.save()
        
        if page_attachment:
            page_message.page_attachments.add(page_attachment)
            page_message.save()
        
        page_message.seen_by_page = seenPage
        page_message.save()
        
        serializer = PageConversationMessageSerializer(page_message)
        
        serializer_data = serializer.data

        json_data = json.dumps(serializer_data)
        
        pusher_client.trigger(f'{str(pk)}', 'page_message:new', {'message': json_data})
        
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add something here later!...'})
    
@api_view(['POST'])
def user_conversation_send_message_to_page(request, id):
    form = PageMessageForm(request.POST)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)
    
    page_conversation = PageConversation.objects.filter(user=request.user).get(id=id)
    seenUser = SeenUser.objects.create(created_by=request.user)
    
    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if form.is_valid():
        message = form.save(commit=False)
        message.created_by = request.user
        message.conversation = page_conversation
        message.sent_to_page = page_conversation.page
                
        message.save()
        
        if attachment:
            message.attachments.add(attachment)
            message.save()
        
        message.seen_by = seenUser
        message.save()
        
        serializer = PageConversationMessageSerializer(message)
        
        serializer_data = serializer.data
        print(sys.getsizeof(serializer_data))

        json_data = json.dumps(serializer_data)
        
        pusher_client.trigger(f'{str(id)}', 'page_message:new', {'message': json_data})
        
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

    form = AvatarGroupForm(request.FILES, instance=current_user)
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
    
    if messages:
        for message in messages:
            if not message.seen_by.all().filter(created_by=request.user):
                message.seen_by.add(seenUser)
                message.save()
    
        serializer = ConversationMessageSerializer(messages, many=True)
        serializer_data = serializer.data[-1]
        json_data = json.dumps(serializer_data)
            
        pusher_client.trigger(str(pk), 'seen_message', {'message': json_data})
                
        return JsonResponse({'message': serializer.data})
    else:
        return JsonResponse({'message': 'conversation not exists'})

@api_view(['POST'])
def user_set_seen_page_conversation(request, pk):
    user = request.user
    page_conversation = PageConversation.objects.filter(user=user).get(pk=pk)
    
    seenUser = SeenUser.objects.create(created_by=user)
        
    page_messages = page_conversation.page_messages.exclude(created_by=user)
    
    if page_messages:
        for page_message in page_messages:
            if not page_message.seen_by == user:
                page_message.seen_by = seenUser
                page_message.save()
    
        serializer = PageConversationMessageSerializer(page_messages, many=True)
        serializer_data = serializer.data[-1]
        json_data = json.dumps(serializer_data)
            
        pusher_client.trigger(str(pk), 'page_seen_message', {'message': json_data})
                
        return JsonResponse({'message': serializer.data})
    else:
        return JsonResponse({'message': 'conversation not exists'})
    
@api_view(['POST'])
def page_set_seen_page_conversation(request, pk, id):
    page = Page.objects.get(id=id)
    page_conversation = PageConversation.objects.filter(page=page).get(pk=pk)
    
    seenPage = SeenPage.objects.create(created_by=page)
        
    page_messages = page_conversation.page_messages.exclude(created_by_page=page)
    
    if page_messages:
        for page_message in page_messages:
            if not page_message.seen_by_page == page:
                page_message.seen_by_page = seenPage
                page_message.save()
    
        serializer = PageConversationMessageSerializer(page_messages, many=True)
        serializer_data = serializer.data[-1]
        json_data = json.dumps(serializer_data)
            
        pusher_client.trigger(str(pk), 'page_seen_message', {'message': json_data})
                
        return JsonResponse({'message': serializer.data})
    else:
        return JsonResponse({'message': 'conversation not exists'})

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
def page_conversation_delete(request, pk):
    page_conversation = PageConversation.objects.get(pk=pk)
    page_conversation.delete()
    
    return JsonResponse({'message': 'conversation deleted'})

@api_view(['DELETE'])
def group_conversation_delete(request, pk):
    group_conversation = GroupConversation.objects.get(pk=pk)
    group_conversation.delete()
    
    return JsonResponse({'message': 'group conversation deleted'})
    
