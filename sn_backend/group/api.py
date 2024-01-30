from django.db.models import Q
from django.http import JsonResponse
from rest_framework.decorators import api_view

from account.models import User
from page.models import Page
from account.serializers import UserSerializer
from page.serializers import PageSerializer
# from notification.models import NotificationForPage
# from notification.utils import create_notification

from .serializers import QuestionSerializer, RuleSerializer, MemberSerializer, PageMemberSerializer, GroupSerializer, GroupDetailSerializer
from .models import Group, Rule, Question, Member, PageMember
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

        