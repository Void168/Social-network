from django.db.models import Q
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.db.models import Count

from account.models import User
from page.models import Page
from account.serializers import UserSerializer
from page.serializers import PageSerializer
# from notification.models import NotificationForPage
# from notification.utils import create_notification

from .serializers import QuestionSerializer, RuleSerializer, MemberSerializer, PageMemberSerializer, GroupSerializer, GroupDetailSerializer, JoinGroupRequestSerializer
from .models import Group, Rule, Question, Member, PageMember, JoinGroupRequest
from .forms import GroupCreateForm, GroupInfoForm, GroupWebsiteForm

@api_view(['POST'])
def create_group(request):
    current_user = User.objects.get(id=request.user.id)
    form = GroupCreateForm(request.POST)
    
    if form.is_valid():
        member = Member.objects.create(information=current_user)
        group = form.save(commit=False)
        group.admin = request.user
        
        group.members_count = 1
        group.save()
        
        group.members.add(member)

        serializer = GroupSerializer(group)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Failed'})
    
@api_view(['GET'])
def get_your_groups(request):
    try:
        members = Member.objects.filter(Q(information=request.user))
        groups = Group.objects.none()
        
        for member in members:
            group = Group.objects.filter(members__in=list([member]))
            groups = groups | group
        
        serializer = GroupSerializer(groups, many=True)
            
        return JsonResponse(serializer.data, safe=False)
    except Member.DoesNotExist:
        return JsonResponse({'message': 'No group found'})

@api_view(['GET'])
def get_group_detail(request, pk):
    group = Group.objects.get(pk=pk)
    try:
        member = Member.objects.get(Q(information=request.user))
        serializer = GroupDetailSerializer(group)
        return JsonResponse(serializer.data, safe=False)
    except Member.DoesNotExist:
        serializer = GroupSerializer(group)
        return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def check_user_in_group(request, pk):
    group = Group.objects.get(pk=pk)
    members = Member.objects.filter(Q(information=request.user))
    if members.count() > 0:
        for member in members:
            if member not in group.members.all():
                return JsonResponse({'message': 'User not in the group'})
            else:
                return JsonResponse({'message': 'User joined the group'})
    else:
        return JsonResponse({'message': 'User not in the group'})

@api_view(['GET'])
def get_friends_in_group(request, pk):
    try:
        current_user = request.user
        group = Group.objects.get(pk=pk)
        members_in_group = group.members.all()
        list_member_id = []
        
        for member in members_in_group:
            list_member_id.append(member.id)
                    
        friends = current_user.friends.all()
        friends_in_group = Member.objects.none()
        
        for friend in friends:
            friend_members = Member.objects.filter(Q(information=friend))
            friends_in_group = friends_in_group | friend_members
            filter = friends_in_group.filter(Q(id__in=list(list_member_id)))
            
        serializer = MemberSerializer(filter, many=True)
        
        if friends_in_group.count() > 0: 
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse({'message': 'No groups found'})
            
    except Member.DoesNotExist:
        return JsonResponse({'message': 'No friends found'})
        
@api_view(['GET'])
def get_discover_groups(request):
    try:
        members = Member.objects.filter(Q(information=request.user))
        discover_groups = Group.objects.none()
        friends = request.user.friends.all()
        
        for friend in friends:
            friend_members = Member.objects.filter(Q(information=friend))
            for friend_member in friend_members:
                for member in members:
                    discover_group = Group.objects.exclude(members__in=list([member])).filter(members__in=list([friend_member]))
                    discover_groups = discover_groups | discover_group
        
        serializer = GroupSerializer(discover_groups, many=True)
        if discover_groups.count() > 0: 
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse({'message': 'No groups found'})
    except Member.DoesNotExist:
        discover_groups =  Group.objects.none()
        friends = request.user.friends.all()
        for friend in friends:
            try:
                friend_member = Member.objects.get(Q(information=friend))
                discover_group = Group.objects.filter(members__in=list([friend_member]))
                discover_groups = discover_groups | discover_group
            except Member.DoesNotExist:
                pass
            
        serializer = GroupSerializer(discover_groups.distinct(), many=True)
        
        if discover_groups.count() > 0: 
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse({'message': 'No groups found'})

@api_view(['POST'])
def join_public_group(request, pk):
    group = Group.objects.get(pk=pk)
    
    member = Member.objects.create(information=request.user)
    
    group.members.add(member)
    group.members_count = group.members_count + 1
    group.save()
    
    return JsonRespone({'message': 'Joined group successfully'})

@api_view((['GET']))
def get_join_group_requests(request, pk):
    current_user = request.user
    group = Group.objects.get(pk=pk)
    
    requests = []
    
    requests = JoinGroupRequest.objects.filter(created_for=group, status=JoinGroupRequest.PENDING)

    serializer = JoinGroupRequestSerializer(requests, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def send_join_request_private_group(request, pk):
    current_user = request.user
    group = Group.objects.get(pk=pk)
    
    check1 = JoinGroupRequest.objects.filter(created_for=group).filter(created_by=current_user)
    
    check2 = JoinGroupRequest.objects.filter(created_for=group).filter(created_by=current_user).filter(status=JoinGroupRequest.REJECTED)

    if not check1:
        join_request = JoinGroupRequest.objects.create(created_for=group, created_by=current_user)
                
        return JsonResponse({'message': 'Join group request created'})
    if check2:
        return JsonResponse({'message': 'Join group request created'})
    else:
        return JsonResponse({'message': 'Join group request already sent'})

@api_view(['POST'])
def handle_join_request(request, pk, status, id):
    request_user = User.objects.get(id=id)
    group = Group.objects.get(pk=pk)
    
    join_request = JoinGroupRequest.objects.filter(created_for=group).get(created_by=request_user)
    join_request.status = status
    join_request.save()

    if status == 'accepted':
        member = Member.objects.create(information=request_user)
        group.members.add(member)
        group.members_count = group.members_count + 1
        group.save()
        
        # notification = Notification.objects.create(
        #     body=f'{sent_user.name} đã đồng ý lời mời kết bạn',
        #     type_of_notification='accepted_friend_request',
        #     created_by=request.user,
        #     created_for=sent_user
        # )
        
        JoinGroupRequest.objects.filter(status='accepted').delete()
        
        # serializer_notification = NotificationSerializer(notification)
        
        # serializer_data = serializer_notification.data

        # json_data = json.dumps(serializer_data)
        # pusher_client.trigger(f'{request.user.id}-notification', 'accepted-friendship-notification:new', {'notification': json_data})
        
        return JsonResponse({'message': 'Request accepted'})
    if status == 'rejected':
        JoinGroupRequest.objects.filter(status='rejected').delete()

        return JsonResponse({'message': 'Request rejected'})

@api_view(['POST'])
def change_group_info(request, pk):
    group = Group.objects.get(pk=pk)
    form = GroupInfoForm(data=request.POST, instance=group)
    
    if form.is_valid() and group.admin == request.user:
        group = form.save()
        
        serializer = GroupDetailSerializer(group)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Failed'})
    
@api_view(['POST'])
def change_group_website(request, pk):
    group = Group.objects.get(pk=pk)
    form = GroupWebsiteForm(data=request.POST, instance=group)
    
    if form.is_valid() and group.admin == request.user:
        group = form.save()
        
        serializer = GroupDetailSerializer(group)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Failed'})
    
@api_view(['POST'])
def set_show_group(request, pk):
    group = Group.objects.get(pk=pk)
    show_group = request.data.get('show_group')
    
    group.show_group = show_group
    group.save()

    serializer = GroupDetailSerializer(group)

    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def set_request_join_group(request, pk):
    group = Group.objects.get(pk=pk)
    anyone_can_join = request.data.get('anyone_can_join')
    
    group.anyone_can_join = anyone_can_join
    group.save()

    serializer = GroupDetailSerializer(group)

    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def set_anonymous_post(request, pk):
    group = Group.objects.get(pk=pk)
    anonymous_post = request.data.get('anonymous_post')
    
    group.anonymous_post = anonymous_post
    group.save()

    serializer = GroupDetailSerializer(group)

    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def set_anyone_can_post(request, pk):
    group = Group.objects.get(pk=pk)
    anyone_can_post = request.data.get('anyone_can_post')
    
    group.anyone_can_post = anyone_can_post
    group.save()

    serializer = GroupDetailSerializer(group)

    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def set_pending_post(request, pk):
    group = Group.objects.get(pk=pk)
    pending_post = request.data.get('pending_post')
    
    group.pending_post = pending_post
    group.save()

    serializer = GroupDetailSerializer(group)

    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def set_anyone_can_poll(request, pk):
    group = Group.objects.get(pk=pk)
    anyone_can_poll = request.data.get('anyone_can_poll')
    
    group.anyone_can_poll = anyone_can_poll
    group.save()

    serializer = GroupDetailSerializer(group)

    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def group_add_moderators(request, pk):
    # other_user_id =request.data.get('otherUser')
    
    list_moderators_id = request.data.get('moderators')
    members = Member.objects.filter(Q(id__in=list(list_moderators_id)))
    group = Group.objects.get(pk=pk)
    
    for member in members:
        group.moderators.add(member)
    
    # if other_user_id != "":
    #     other_user = User.objects.get(id=other_user_id)
    
    #     group_conversation.users.add(other_user)
    
    group.save()
    
    serializer = GroupDetailSerializer(group)
    
    return JsonResponse({'message':'moderators update', 'group': serializer.data})

@api_view(['POST'])
def remove_moderator(request, pk, id):
    group = Group.objects.get(pk=pk)
    moderator = Member.objects.get(id=id)
    
    if request.user == group.admin:
        group.moderators.remove(moderator)
        
        group.save()
        
        serializer = GroupDetailSerializer(group)
        
        return JsonResponse({'message':'moderator removed', 'group': serializer.data})
    else:
        return JsonResponse({'error':"You don't have permission to do that"})