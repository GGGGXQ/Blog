from django.http import JsonResponse
from django.conf import settings
from django.core.signing import Signer
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import ProfileForm, SignupForm
from .models import User, FriendshipRequest
from .serializers import UserSerializers, FriendshipRequestSerializer
from notification.utils import create_notification


@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        'avatar': request.user.get_avatar()
    })


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
        'user': UserSerializers(user).data,
        'friends': UserSerializers(friends, many=True).data,
        'requests': requests
    }, safe=False)


@api_view(['GET'])
def my_friendship_suggetions(request):
    serializer = UserSerializers(request.user.people_you_may_know.all(), many=True)
    return JsonResponse(serializer.data, safe=False)


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

        
        signer = Signer()
        token = signer.sign(f"{user.email}|{user.id}")

        url = f"{settings.WEBSITE_URL}/activateemail/?token={token}"

    else:
        message = form.errors.as_json()
    print(message)

    return JsonResponse({'message': message}, safe=False)


@api_view(['POST'])
def editprofile(request):
    user = request.user
    form = ProfileForm(request.data, request.FILES, instance=user)

    if form.is_valid():
        form.save()

    serializer = UserSerializers(user)

    return JsonResponse({'message': '修改已更新', 'user': serializer.data}, status=200)


@api_view(['POST'])
def editpassword(request):
    user = request.user
    
    form = PasswordChangeForm(data=request.POST, user=user)

    if form.is_valid():
        form.save()

        return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': form.errors.as_json()}, safe=False)


@api_view(['POST'])
def send_friendship_request(request, pk):
    user = get_object_or_404(User, pk=pk) 

    # 检查是否已经存在好友请求，无论是自己发的还是对方发的
    existing_request_sent = FriendshipRequest.objects.filter(created_for=user, created_by=request.user).exists()
    existing_request_received = FriendshipRequest.objects.filter(created_for=request.user, created_by=user).exists()

    if existing_request_sent:
        return JsonResponse({'message': 'You have already sent a friendship request to this user.'})

    if existing_request_received:
        return JsonResponse({'message': 'The user has already sent you a friendship request.'})

    friendrequest = FriendshipRequest.objects.create(created_for=user, created_by=request.user)
    notification = create_notification(request, 'new_friendrequest', friendrequest_id=friendrequest.id)
    return JsonResponse({'message': 'Friendship request sent successfully.'})

@api_view(['POST'])
def handle_request(request, pk, status):
    user = User.objects.get(pk=pk)
    friendship_request = FriendshipRequest.objects.filter(created_for=request.user).get(created_by=user)

    friendship_request.status = status
    friendship_request.save()

    user.friends.add(request.user)
    user.friends_count = user.friends_count + 1
    user.save()

    request_user = request.user
    request_user.friends_count = request_user.friends_count + 1
    request_user.save()
    
    notification = create_notification(request, 'accepted_friendrequest', friendrequest_id=friendship_request.id)

    return JsonResponse({'message': 'friendship request updated'})
