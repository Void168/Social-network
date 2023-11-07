from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from notification.utils import create_notification

from .forms import SignupForm, ProfileForm, CoverImageForm, RelationshipForm
from .models import User, FriendshipRequest
from .serializers import UserSerializer, FriendshipRequestSerializer

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
    
    if user == request.user:
        requests = FriendshipRequest.objects.filter(created_for=request.user, status=FriendshipRequest.SENT)
        requests = FriendshipRequestSerializer(requests, many=True)
        requests = requests.data
       
    friends = user.friends.all()   
     
    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many=True).data,
        'requests': requests
    }, safe=False)
    
@api_view(['GET'])
def my_friendship_suggestions(request):
    serializer = UserSerializer(request.user.people_you_may_know.all(), many=True)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def edit_profile(request):
    user = request.user
    email = request.data.get('email')
    
    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return JsonResponse({'message': 'Email đã được đăng ký. Vui lòng thử lại'})
    else:
        # print(request.FILES)
        # print(request.POST)
        form = ProfileForm(request.POST, request.FILES, instance=user)
        
        if form.is_valid():
            form.save()
        
        serializer = UserSerializer(user)
        
        return JsonResponse({'message': 'information updated', 'user': serializer.data})
    
@api_view(['POST'])
def set_relationship(request):
    user = request.user
    
    print(request.POST)
    form = RelationshipForm(data=request.POST, instance=user)
    print(form.is_valid())
    if form.is_valid():
        form.save()
        user.save()
        
    serializer = UserSerializer(user)
        
    return JsonResponse({'message': 'information updated', 'user': serializer.data})

@api_view(['GET'])
def relationship_detail(request, id):
    return JsonResponse({'message': 'hello'})

@api_view(['POST'])
def edit_cover_image(request):
    user = request.user
    
    form = CoverImageForm(request.POST, request.FILES, instance=user)
    
    if form.is_valid:
        form.save()
    
    serializer = UserSerializer(user)
    
    return JsonResponse({'message': 'cover image updated'})

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
    user = User.objects.get(pk=pk)
    
    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)
    
    check3 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user).filter(status=FriendshipRequest.REJECTED)
    check4 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user).filter(status=FriendshipRequest.REJECTED)
    
    if not check1 and not check2:
        friendrequest = FriendshipRequest.objects.create(created_for=user, created_by=request.user)
        
        notification = create_notification(request, 'new_friend_request', friendrequest_id=friendrequest.id)

        
        return JsonResponse({'message': 'friendship request created'})
    if check3 and check4:
        return JsonResponse({'message': 'friendship request created'})
    else:
        return JsonResponse({'message': 'request already sent'})

@api_view(['POST'])
def handle_request(request, pk, status):
    user = User.objects.get(pk=pk)
    friendship_request = FriendshipRequest.objects.filter(created_for=request.user).get(created_by=user)
    friendship_request.status = status
    friendship_request.save()

    if status == 'accepted':
        user.friends.add(request.user)
        user.friends_count = user.friends_count + 1
        user.save()
        
        request_user = request.user
        request_user.friends_count = request_user.friends_count + 1
        request_user.save()
        
        notification = create_notification(request, 'accepted_friend_request', friendrequest_id=friendship_request.id)
    
    if status == 'rejected':
        FriendshipRequest.objects.filter(status='rejected').delete()


    return JsonResponse({'message': 'friendship request updated'})