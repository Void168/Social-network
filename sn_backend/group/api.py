from django.db.models import Q
from django.http import JsonResponse
from rest_framework.decorators import api_view

from account.models import User
from page.models import Page
from account.serializers import UserSerializer
from page.serializers import PageSerializer
# from notification.models import NotificationForPage
# from notification.utils import create_notification

from .serializers import QuestionSerializer, RuleSerializer, MemberSerializer, PageMemberSerializer, GroupSerializer, GroupDetailSerializer, JoinGroupRequestSerializer
from .models import Group, Rule, Question, Member, PageMember, JoinGroupRequest
from .forms import GroupCreateForm

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
        member = Member.objects.get(Q(information=request.user))
        groups = Group.objects.filter(members__in=list([member]))
        
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
def get_discover_groups(request):
    try:
        member = Member.objects.get(Q(information=request.user))
        discover_groups = Group.objects.none()
        friends = request.user.friends.all()
        
        for friend in friends:
            friend_member = Member.objects.get(Q(information=request.user))
            discover_group = Group.objects.exclude(members__in=list([member])).filter(members__in=list([friend_member]))
            discover_groups = discover_groups | discover_group
        
        serializer = GroupSerializer(discover_groups, many=True)
        if discover_groups.count() > 0: 
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse({'message': 'No group found'})
    except Member.DoesNotExist:
        discover_groups =  Group.objects.none()
        friends = request.user.friends.all()
        friend_member = Member.objects.get(Q(information=friends[1]))
        for friend in friends:
            try:
                friend_member = Member.objects.get(Q(information=friend))
                discover_group = Group.objects.filter(members__in=list([friend_member]))
                discover_groups = discover_groups | discover_group
            except Member.DoesNotExist:
                pass
            
        serializer = GroupSerializer(discover_groups, many=True)
        
        if discover_groups.count() > 0: 
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse({'message': 'No group found'})

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
