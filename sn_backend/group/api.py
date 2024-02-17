from django.db.models import Q
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.db.models import Count

from django.utils.timesince import timesince

from datetime import datetime, timezone, timedelta

from account.models import User
from page.models import Page
from post.models import GroupPost, MemberLike, MemberComment
from account.serializers import UserSerializer
from page.serializers import PageSerializer
# from notification.models import NotificationForPage
# from notification.utils import create_notification

from .serializers import QuestionSerializer, RuleSerializer, MemberSerializer, PageMemberSerializer, GroupSerializer, GroupDetailSerializer, JoinGroupRequestSerializer, QuestionSerializer
from post.serializers import GroupPostSerializer, MemberLikeSerializer, MemberCommentSerializer
from .models import Group, Rule, Question, Member, PageMember, JoinGroupRequest, Answer
from .forms import GroupCreateForm, GroupInfoForm, GroupWebsiteForm, GroupQuestionForm, GroupCoverImageForm, GroupRuleForm

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

@api_view(['POST'])
def edit_group_cover_image(request, pk):
    group = Group.objects.get(pk=pk)
    
    form = GroupCoverImageForm(request.POST, request.FILES, instance=group)
    
    if form.is_valid:
        form.save()
    
    serializer = GroupSerializer(group)
    
    return JsonResponse({'message': 'group cover image updated'})

@api_view(['GET'])
def get_group_detail(request, pk):
    group = Group.objects.get(pk=pk)
    try:
        member = Member.objects.filter(Q(information=request.user))
        serializer = GroupDetailSerializer(group)
        return JsonResponse(serializer.data, safe=False)
    except Member.DoesNotExist:
        serializer = GroupSerializer(group)
        return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def get_current_member(request, pk):
    group = Group.objects.get(pk=pk)
    members = Member.objects.filter(Q(information=request.user))
    
    group_members = group.members.all()
    if members.count() > 0:
        for member in members:
            if member not in group_members:
                # return JsonResponse({'message': 'User not in the group'})
                pass
            else:
                serializer = MemberSerializer(member)
                return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'message': 'User not in the group'})

@api_view(['GET'])
def check_user_in_group(request, pk):
    group = Group.objects.get(pk=pk)
    members = Member.objects.filter(Q(information=request.user))
    if members.count() > 0:
        for member in members:
            if member not in group.members.all():
                # return JsonResponse({'message': 'User not in the group'})
                pass
            else:
                return JsonResponse({'message': 'User joined the group'})
                break
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
    members = Member.objects.filter(Q(information=request.user))
    friends = request.user.friends.all()
    discover_groups = Group.objects.none()
    if members:
        for friend in friends:
            friend_members = Member.objects.filter(Q(information=friend))
            if friend_members:
                for friend_member in friend_members:
                    discover_group = Group.objects.exclude(members__in=list(members)).filter(members__in=list([friend_member]))
                        
                    discover_groups = discover_groups | discover_group
            else:
                continue
        
        serializer = GroupSerializer(discover_groups.distinct(), many=True)
        if discover_groups.count() > 0: 
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse({'message': 'No groups found'})
    else:
        for friend in friends:
            friend_members = Member.objects.filter(Q(information=friend))
            if friend_members:
                for friend_member in friend_members:
                    discover_group = Group.objects.filter(members__in=list([friend_member]))
                    discover_groups = discover_groups | discover_group
            else:
                continue
            
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
    
    return JsonResponse({'message': 'Joined group successfully'})

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
        join_request = JoinGroupRequest.objects.create(created_for=group, created_by=current_user, status='pending')
                
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
        
        # JoinGroupRequest.objects.filter(status='accepted').delete()
        
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
    
@api_view(['POST'])
def kick_member(request, pk, id):
    group = Group.objects.get(pk=pk)
    user = User.objects.get(id=id)
    members = Member.objects.filter(Q(information=user))
    
    for member in members:
        if member in group.members.all():
            group.members.remove(member)
            member.delete()
            group.members_count = group.members_count - 1
            group.save()
            
            return JsonResponse({'message': 'Member has been kicked'})
        else:
            continue
        
@api_view(['POST'])
def leave_group(request, pk):
    group = Group.objects.get(pk=pk)
    members = Member.objects.filter(Q(information=request.user))
    
    for member in members:
        if member in group.members.all():
            group.members.remove(member)
            member.delete()
            group.members_count = group.members_count - 1
            group.save()
            
            return JsonResponse({'message': 'Leaved group'})
        else:
            continue

@api_view(['POST'])
def create_questions(request, pk):
    group = Group.objects.get(pk=pk)
    form = GroupQuestionForm(request.POST)
    
    if form.is_valid():
        question = form.save(commit=False)
        question.created_by = group
        
        question.save()

        serializer = QuestionSerializer(question)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Failed'})
    
@api_view(['POST'])
def create_answer(request, pk):
    group = Group.objects.get(pk=pk)
    questions = Question.objects.filter(created_by=group)
    join_request = JoinGroupRequest.objects.get(Q(created_by=request.user, created_for=group))
    
    answer1 = request.data.get('answer1')
    answer2 = request.data.get('answer2')
    answer3 = request.data.get('answer3')
    if join_request.answers.count() == 0:
        if questions.count() > 0:
            question1 = questions[0]
            if questions.count() > 1:
                question2 = questions[1]
                if questions.count() > 2:
                    question3 = questions[2]
                    
        if answer1 and question1:
            answer_1 = Answer.objects.create(
                body=answer1,
                created_by=request.user,
                question=question1
            )
            join_request.answers.add(answer_1)
            
        if answer2 and question2:
            answer_2 = Answer.objects.create(
                body=answer2,
                created_by=request.user,
                question=question2
            )
            join_request.answers.add(answer_2)
            
        if answer3 and question3:
            answer_3 = Answer.objects.create(
                body=answer3,
                created_by=request.user,
                question=question3
            )
            join_request.answers.add(answer_3)
        
    join_request.save()
    
    serializer = JoinGroupRequestSerializer(join_request)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def get_group_questions(request, pk):
    group = Group.objects.get(pk=pk)

    questions = Question.objects.filter(created_by=group)

    serializer = QuestionSerializer(questions, many=True)

    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def update_group_question(request, pk):
    question = Question.objects.get(pk=pk)
    form = GroupQuestionForm(request.POST, instance=question)
    
    if form.is_valid():
        form.save()
        
    serializer = QuestionSerializer(question)
        
    return JsonResponse({'message': 'Question updated', 'question': serializer.data})

@api_view(['POST'])
def delete_group_question(request, pk):
    question = Question.objects.get(pk=pk)
    question.delete()

    return JsonResponse({'message': 'Question deleted'})

@api_view(['POST'])
def update_last_access(request, pk):
    group = Group.objects.get(pk=pk)
    
    members = Member.objects.filter(information=request.user)
    
    group_members = group.members.all()
    
    current_member = Member.objects.none()
    
    if members.count() > 0:
        for member in members:
            if member in group_members:
                current_member = member
            else:
                continue
            
    timezone_offset = 7.0
    tzinfo = timezone(timedelta(hours=timezone_offset))
    current_time = datetime.now(tzinfo)

    current_member.last_access = current_time
    current_member.last_access_formatted = timesince(current_time)
    current_member.save()
    
    return JsonResponse({'message': 'Access group'}) 

@api_view(['POST'])
def create_rule(request, pk):
    group = Group.objects.get(pk=pk)
    form = GroupRuleForm(request.POST)
    
    if form.is_valid():
        rule = form.save(commit=False)
        rule.created_by = group
        
        rule.save()

        serializer = RuleSerializer(rule)

        return JsonResponse({'message': 'Created rule', 'rule': serializer.data}, safe=False)
    else:
        return JsonResponse({'error': 'Failed'})
    
@api_view(['GET'])
def get_rules(request, pk):
    group = Group.objects.get(pk=pk)
    
    rules = Rule.objects.filter(Q(created_by=group))
    
    serializer = RuleSerializer(rules, many=True)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def delete_rule(request, pk):
    rule = Rule.objects.get(pk=pk)
    rule.delete()
    
    return JsonResponse({'message': 'Rule deleted'})

@api_view(['GET'])
def get_group_overview(request, pk):
    group = Group.objects.get(pk=pk)
    join_requests = JoinGroupRequest.objects.filter(created_for=group)
    admin_member = Member.objects.get(information=group.admin)
    moderators = group.moderators.all()
    
    group_posts = GroupPost.objects.filter(Q(group=group, pending=False))
    pending_posts = GroupPost.objects.filter(Q(group=group, pending=True)).exclude(Q(created_by=admin_member) | Q(created_by__in=moderators))
        
    week_ago = datetime.now() - timedelta(days=7)
    month_ago = datetime.now() - timedelta(days=28)
    # sixty_ago = datetime.now() - timedelta(days=60)
    
    new_members_in_seven_days = []
    new_members_in_twenty_eight_days = []
    # new_members_in_sixty_days = []
    
    new_posts_in_seven_days = []
    new_posts_in_twenty_eight_days = []
    
    new_likes_in_seven_days = 0
    new_likes_in_twenty_eight_days = 0
    
    new_comments_in_seven_days = 0
    new_comments_in_twenty_eight_days = 0
    
    for member in group.members.all():
        if member.date_join_group.timestamp() > week_ago.timestamp() and member.date_join_group.timestamp() < datetime.now().timestamp():
            new_members_in_seven_days.append(member)
        if member.date_join_group.timestamp() > month_ago.timestamp() and member.date_join_group.timestamp() < datetime.now().timestamp():
            new_members_in_twenty_eight_days.append(member)
        # if member.date_join_group.timestamp() > sixty_ago.timestamp() and member.date_join_group.timestamp() < datetime.now().timestamp():
        #     new_members_in_sixty_days.append(member)
    
    for group_post in group_posts:
        if group_post.created_at.timestamp() > week_ago.timestamp() and group_post.created_at.timestamp() < datetime.now().timestamp():
            new_posts_in_seven_days.append(group_post)
            new_likes_in_seven_days = new_likes_in_seven_days + group_post.likes_count
            new_comments_in_seven_days = new_comments_in_seven_days + group_post.comments_count
        if group_post.created_at.timestamp() > month_ago.timestamp() and group_post.created_at.timestamp() < datetime.now().timestamp():
            new_posts_in_twenty_eight_days.append(group_post)
            new_likes_in_twenty_eight_days = new_likes_in_twenty_eight_days + group_post.likes_count
            new_comments_in_twenty_eight_days = new_comments_in_twenty_eight_days + group_post.comments_count
    
    return JsonResponse({
        'memberSevenDays': len(new_members_in_seven_days),
        'memberTwentyEightDays': len(new_members_in_twenty_eight_days),
        # 'memberSixtyDays': len(new_members_in_sixty_days),
        'postSevenDays': len(new_posts_in_seven_days),
        'postTwentyEightDays': len(new_posts_in_twenty_eight_days),
        'likeSevenDays': new_likes_in_seven_days,
        'likeTwentyEightDays': new_likes_in_twenty_eight_days,
        'commentSevenDays': new_comments_in_seven_days,
        'commentTwentyEightDays': new_comments_in_twenty_eight_days,
        'joinRequests': len(join_requests),
        'pendingPosts': len(pending_posts)
        })
    
@api_view(['GET'])
def get_group_join_requests_growth(request, pk):
    group = Group.objects.get(pk=pk)
    sixty_ago = (datetime.now() - timedelta(days=60))
    today = datetime.now()
    
    join_requests = JoinGroupRequest.objects.filter(Q(created_for=group, created_at__range=(sixty_ago, today)))
    
    join_requests_serializer = JoinGroupRequestSerializer(join_requests, many=True)
            
    return JsonResponse({'joinRequests': join_requests_serializer.data})

@api_view(['GET'])
def get_group_posts_growth(request, pk):
    group = Group.objects.get(pk=pk)
    sixty_ago = (datetime.now() - timedelta(days=60))
    today = datetime.now()
    
    posts = GroupPost.objects.filter(Q(group=group, created_at__range=(sixty_ago, today)))
    
    posts_serializer = GroupPostSerializer(posts, many=True)
            
    return JsonResponse({'groupPosts': posts_serializer.data})

@api_view(['GET'])
def get_group_likes_growth(request, pk):
    group = Group.objects.get(pk=pk)
    sixty_ago = (datetime.now() - timedelta(days=60))
    today = datetime.now()
    
    likes = MemberLike.objects.none()
    
    posts = GroupPost.objects.filter(Q(group=group, created_at__range=(sixty_ago, today)))

    for post in posts:
        likes = likes | post.likes.all()
    
    likes_serializer = MemberLikeSerializer(likes, many=True)
            
    return JsonResponse({'likes': likes_serializer.data})

@api_view(['GET'])
def get_group_comments_growth(request, pk):
    group = Group.objects.get(pk=pk)
    sixty_ago = (datetime.now() - timedelta(days=60))
    today = datetime.now()
    
    comments = MemberComment.objects.none()
    
    posts = GroupPost.objects.filter(Q(group=group, created_at__range=(sixty_ago, today)))

    for post in posts:
        comments = comments | post.comments.all()
    
    comment_serializer = MemberCommentSerializer(comments, many=True)
            
    return JsonResponse({'comments': comment_serializer.data})

@api_view(['GET'])
def get_group_active_member(request, pk):
    group = Group.objects.get(pk=pk)
    sixty_ago = (datetime.now() - timedelta(days=60))
    today = datetime.now()
    
    group_members = group.members.all()
    
    access_members = []
    
    for group_member in group_members:
        if group_member.last_access.timestamp() > sixty_ago.timestamp() and group_member.last_access.timestamp() <today.timestamp():
            access_members.append(group_member)
    
    serializer = MemberSerializer(access_members, many=True)
    
    return JsonResponse({'activeMembers': serializer.data})