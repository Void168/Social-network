from django.db.models import Q
from django.http import JsonResponse
from rest_framework.decorators import api_view

from account.models import User
from page.models import Page
from account.serializers import UserSerializer
from page.serializers import PageSerializer
# from notification.models import NotificationForPage
# from notification.utils import create_notification

from .serializers import QuestionSerializer, RuleSerializer, MemberSerializer, PageMemberSerializer, GroupSerializer
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
    return JsonResponse({'error': 'Failed'})