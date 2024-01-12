from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.core.mail import send_mail
from django.http import JsonResponse
import json
from .pusher import pusher_client

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from notification.utils import create_notification

from .forms import SignupForm, ProfileForm, CoverImageForm, AvatarForm, RelationshipForm, BiographyForm, HomeTownForm, LivingCityForm
from .models import User, FriendshipRequest, RelationshipRequest
from notification.models import Notification
from .serializers import UserSerializer, FriendshipRequestSerializer, RelationshipRequestSerializer
from notification.serializers import NotificationSerializer

@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        'avatar': request.user.get_avatar(),
        'cover_image': request.user.get_cover_image()
    })

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'
    
    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })
    
    if form.is_valid():
        user = form.save()
        user.is_active = False
        user.save()
        
        url= f'http://127.0.0.1:8000/activate-email/?email={user.email}&id={user.id}'
        
        send_mail(
            "Xác thực tài khoản của bạn",
            f"Link xác thực tài khoản của bạn: {url}",
            'settings.EMAIL_HOST_USER',
            [user.email],
            fail_silently=False,
        )
    
    else:
        message = 'error'
    
    return JsonResponse({'status': message}, safe=False)

@api_view(['GET'])
def friends(request, pk):
    user = User.objects.get(pk=pk)
    requests = []
    
    requests = FriendshipRequest.objects.filter(created_for=request.user, status=FriendshipRequest.SENT)
    requests = FriendshipRequestSerializer(requests, many=True)
    requests = requests.data
    
    request_by = FriendshipRequest.objects.filter(created_by=request.user, status=FriendshipRequest.SENT)
    serializer = FriendshipRequestSerializer(request_by, many=True)
    
    user_followers = user.followers.all()
    user_following = user.following.all()
       
    friends = user.friends.all()
     
    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many=True).data,
        'requests': requests,
        'request_by': serializer.data,
        'followers':UserSerializer(user_followers, many=True).data,
        'following':UserSerializer(user_following, many=True).data,
    }, safe=False)
    
@api_view(['GET'])
def my_friendship_suggestions(request):
    serializer = UserSerializer(request.user.people_you_may_know.all(), many=True)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def user_info(request, pk):
    user = User.objects.get(pk=pk)
    
    return JsonResponse({
        'user': UserSerializer(user).data,
    }, safe=False)

@api_view(['POST'])
def edit_profile(request):
    user = request.user
    email = request.data.get('email')
    name = request.data.get('name')
    
    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return JsonResponse({'message': 'Email đã được đăng ký. Vui lòng thử lại'})
    if User.objects.exclude(id=user.id).filter(name=name).exists():
        return JsonResponse({'message': 'Tên đã được sử dụng. Vui lòng thử lại'})
    else:
        form = ProfileForm(request.POST, instance=user)
        
        if form.is_valid():
            form.save()
        
        serializer = UserSerializer(user)
        
        return JsonResponse({'message': 'information updated', 'user': serializer.data})

@api_view(['POST'])
def set_biography(request):
    current_user = request.user
    
    form = BiographyForm(data=request.POST, instance=current_user)
    
    if form.is_valid():
        form.save()
        
        current_user.save()
    
        serializer = UserSerializer(current_user)
    
        return JsonResponse(serializer.data)
    else: 
        return JsonResponse({'message':'Failed'})

@api_view(['POST'])
def set_hometown(request):
    current_user = request.user
    
    form = HomeTownForm(data=request.POST, instance=current_user)
    
    if form.is_valid():
        form.save()
        
        current_user.save()
    
        serializer = UserSerializer(current_user)
    
        return JsonResponse(serializer.data)
    else: 
        return JsonResponse({'message':'Failed'})
    
@api_view(['POST'])
def set_livingcity(request):
    current_user = request.user
    
    form = LivingCityForm(data=request.POST, instance=current_user)
    
    if form.is_valid():
        form.save()
        
        current_user.save()
    
        serializer = UserSerializer(current_user)
    
        return JsonResponse(serializer.data)
    else: 
        return JsonResponse({'message':'Failed'})

@api_view(['GET'])
def relationship(request, pk):
    user = User.objects.get(pk=pk)
    relationshipRequest = {}
    
    if user == request.user:
        relationshipRequest = RelationshipRequest.objects.filter(created_for=request.user, status=RelationshipRequest.SENT)
        relationshipRequest = RelationshipRequestSerializer(relationshipRequest, many=True)
        relationshipRequest = relationshipRequest.data
            
    return JsonResponse({
        'user': UserSerializer(user).data,
        'request': relationshipRequest
    }, safe=False)

@api_view(['POST'])
def set_relationship(request):
    current_user = request.user
    
    form = RelationshipForm(data=request.POST, instance=current_user)
    
    if form.is_valid():
        form.save()
        
        current_user.save()
    
        serializer = UserSerializer(current_user)
    
        return JsonResponse(serializer.data)
    else: 
        return JsonResponse({'message':'Failed'})


@api_view(['POST'])
def send_relationship_request(request, pk):
    user = User.objects.get(pk=pk)
    form = RelationshipForm(data=request.POST, instance=user)
    relationship_type = form.data["relationship_status"]
    received_user = User.objects.get(id=form.data["partner"])
    
    check1 = RelationshipRequest.objects.filter(created_for=received_user).filter(created_by=user)
    check2 = RelationshipRequest.objects.filter(created_for=user).filter(created_by=received_user)
    
    check3 = RelationshipRequest.objects.filter(created_for=request.user).filter(created_by=user).filter(status=RelationshipRequest.REJECTED)
    check4 = RelationshipRequest.objects.filter(created_for=user).filter(created_by=request.user).filter(status=RelationshipRequest.REJECTED)
    
    if received_user.partner != '':
        return JsonResponse({'message': "don't be a third person"})
    
    if not check1 and not check2:
        relationship_request = RelationshipRequest.objects.create(created_for=user, created_by=request.user, relationship_type=relationship_type)
        
        notification = create_notification(request, 'new_relationship_request', relationship_request_id=relationship_request.id)

        serializer_notification = NotificationSerializer(notification)
        
        serializer_data = serializer_notification.data

        json_data = json.dumps(serializer_data)
                
        pusher_client.trigger(f'{request.user.id}-notification', 'relationship-request-notification:new', {'notification': json_data})
        
        return JsonResponse({'message': 'relationship request created'})
    if check3 and check4:
        return JsonResponse({'message': 'relationship request created'})
    
    else:
        return JsonResponse({'message': 'request already sent'})

@api_view(['POST'])
def handle_request_relationship(request, pk, status):
    sent_user = User.objects.get(pk=pk)
        
    relationship_request = RelationshipRequest.objects.filter(created_for=request.user).get(created_by=sent_user)
    relationship_request.status = status
    relationship_request.save()

    partner = User.objects.get(Q(email=relationship_request.created_for))
    
    if status == 'accepted':
        sent_user.partner = partner.id
        sent_user.relationship_status = relationship_request.relationship_type
        
        partner.partner = sent_user.id
        partner.relationship_status = relationship_request.relationship_type
            
        partner.save()
            
        sent_user.save()
        
        notification = Notification.objects.create(
            body=f'{sent_user.name} đã đồng ý',
            type_of_notification='accepted_relationship_request',
            created_by=request.user,
            created_for=sent_user
        )
        
        serializer_notification = NotificationSerializer(notification)
        
        serializer_data = serializer_notification.data

        json_data = json.dumps(serializer_data)
        pusher_client.trigger(f'{request.user.id}-notification', 'accepted-relationship-notification:new', {'notification': json_data})
    
    if status == 'rejected':
        RelationshipRequest.objects.filter(status='rejected').delete()

    return JsonResponse({'message': 'relationship request updated'})

@api_view(['DELETE'])
def delete_relationship(request):
    current_user = request.user
    print(current_user)
    
    relationship_request = RelationshipRequest.objects.filter(created_for=request.user)
    relationship_request.delete()
    
    current_user = User.objects.get(email=current_user)
    partner_id = User.objects.get(email=current_user).partner
    
    current_user.relationship_status = ''
    current_user.partner = ''
    current_user.save()
    
    if partner_id != '' and partner_id != 'null':
        partner = User.objects.get(id=partner_id)
        partner.partner = ''
        partner.relationship_status = ''
        partner.save()
        
    serializer = UserSerializer(current_user)
    
    return JsonResponse(serializer.data)


@api_view(['POST'])
def edit_cover_image(request):
    user = request.user
    
    form = CoverImageForm(request.POST, request.FILES, instance=user)
    
    if form.is_valid:
        form.save()
    
    serializer = UserSerializer(user)
    
    return JsonResponse({'message': 'cover image updated'})

@api_view(['POST'])
def edit_avatar(request):
    user = request.user

    form = AvatarForm(request.POST, request.FILES, instance=user)
    if form.is_valid:
        form.save()
    
    serializer = UserSerializer(user)
    
    return JsonResponse({'message': 'avatar updated'})

@api_view(['POST'])
def edit_password(request):
    user = request.user
    
    form = PasswordChangeForm(data=request.POST, user=user)
    
    if form.is_valid():
        form.save()
        
        return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': form.errors.as_json()}, safe=False)

@api_view(['POST'])
def send_friendship_request(request, pk):
    sent_user = User.objects.get(pk=pk)
    current_user = request.user
    
    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=sent_user)
    check2 = FriendshipRequest.objects.filter(created_for=sent_user).filter(created_by=request.user)
    
    check3 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=sent_user).filter(status=FriendshipRequest.REJECTED)
    check4 = FriendshipRequest.objects.filter(created_for=sent_user).filter(created_by=request.user).filter(status=FriendshipRequest.REJECTED)

    if not check1 and not check2:
        sent_user.followers.add(request.user)
        current_user.following.add(sent_user)
        sent_user.followers_count = sent_user.followers_count + 1
        sent_user.save()
        
        friendrequest = FriendshipRequest.objects.create(created_for=sent_user, created_by=request.user)
        
        notification = create_notification(request, 'new_friend_request', friendrequest_id=friendrequest.id)

        serializer_notification = NotificationSerializer(notification)
        
        serializer_data = serializer_notification.data

        json_data = json.dumps(serializer_data)
        pusher_client.trigger(f'{request.user.id}-notification', 'send-friendship-notification:new', {'notification': json_data})
        
        return JsonResponse({'message': 'friendship request created'})
    if check3 and check4:
        return JsonResponse({'message': 'friendship request created'})
    else:
        return JsonResponse({'message': 'request already sent'})

@api_view(['POST'])
def handle_request(request, pk, status):
    sent_user = User.objects.get(pk=pk)
    friendship_request = FriendshipRequest.objects.filter(created_for=request.user).get(created_by=sent_user)
    friendship_request.status = status
    friendship_request.save()

    if status == 'accepted':
        sent_user.friends.add(request.user)
        sent_user.friends_count = sent_user.friends_count + 1
        sent_user.save()
        
        request_user = request.user
        request_user.friends_count = request_user.friends_count + 1
        request_user.save()
        
        notification = Notification.objects.create(
            body=f'{sent_user.name} đã đồng ý lời mời kết bạn',
            type_of_notification='accepted_friend_request',
            created_by=request.user,
            created_for=sent_user
        )
        
        FriendshipRequest.objects.filter(status='accepted').delete()
        
        serializer_notification = NotificationSerializer(notification)
        
        serializer_data = serializer_notification.data

        json_data = json.dumps(serializer_data)
        pusher_client.trigger(f'{request.user.id}-notification', 'accepted-friendship-notification:new', {'notification': json_data})
    
    if status == 'rejected':
        FriendshipRequest.objects.filter(status='rejected').delete()


    return JsonResponse({'message': 'friendship request updated'})

@api_view(['POST'])
def delete_friend(request, pk):
    current_user = request.user
    friend_wanna_delete = User.objects.get(pk=pk)
    
    current_user_friends = current_user.friends.all()
    friend_wanna_delete_friends = friend_wanna_delete.friends.all()
    friend_wanna_delete_followers = friend_wanna_delete.followers.all()
    
    if friend_wanna_delete in current_user_friends and current_user in friend_wanna_delete_friends:
    
        current_user.friends.remove(friend_wanna_delete)
        current_user.friends_count = current_user.friends_count - 1
        
        friend_wanna_delete.friends.remove(current_user)
        friend_wanna_delete.friends_count = friend_wanna_delete.friends_count - 1
        
        if current_user in friend_wanna_delete_followers:
            friend_wanna_delete.followers.remove(current_user)
            friend_wanna_delete.followers_count = friend_wanna_delete.followers_count - 1
        
        current_user.save()
        
        friend_wanna_delete.save()
    
        return JsonResponse({'message': 'friendship deleted'})
    
    else:
        return JsonResponse({'message': "Don't have friend with each other"})
    
@api_view(['POST'])
def follow(request, pk):
    current_user = request.user
    user_wanna_follow = User.objects.get(pk=pk)
    
    current_user_following_list = current_user.following.all()
    user_follow_list = user_wanna_follow.followers.all()
    
    if not current_user in user_follow_list and not user_wanna_follow in current_user_following_list:
    
        user_wanna_follow.followers.add(current_user)
        current_user.following.add(user_wanna_follow)
        
        user_wanna_follow.followers_count = user_wanna_follow.followers_count + 1
        
        user_wanna_follow.save()
    
        return JsonResponse({'message': 'Followed'})
    
    else:
        return JsonResponse({'message': "Failed"})
    
@api_view(['POST'])
def unfollowed(request, pk):
    current_user = request.user
    user_wanna_unfollow = User.objects.get(pk=pk)
    
    user_follow_list = user_wanna_unfollow.followers.all()
    current_user_following_list = current_user.following.all()

    if current_user in user_follow_list and user_wanna_unfollow in current_user_following_list:
        user_wanna_unfollow.followers.remove(current_user)
        current_user.following.remove(user_wanna_unfollow)
        
        user_wanna_unfollow.followers_count = user_wanna_unfollow.followers_count - 1
        
        user_wanna_unfollow.save()
    
        return JsonResponse({'message': 'UnFollowed'})
    
    else:
        return JsonResponse({'message': "Failed"})