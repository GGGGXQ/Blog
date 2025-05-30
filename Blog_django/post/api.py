from json import JSONDecodeError
import json
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from notification.utils import create_notification
from .forms import PostForm, AttachmentForm
from .models import Post, Like, Comment, Trend
from .serializers import CommentSerializer, PostSerializers, PostDetailSerializer, TrendSerializer
from account.models import FriendshipRequest, User
from account.serializers import UserSerializers


@api_view(['GET'])
def post_list(request):
    user = User.objects.get(id=request.user.id)  # 强制刷新用户对象
    friends = user.friends.all()  # 获取最新好友列表
    user_ids = [user.id] + [friend.id for friend in friends]
    posts = Post.objects.filter(created_by_id__in=list(user_ids))
    trend = request.GET.get('trend', '')
    if trend:
        posts = Post.objects.filter(
            Q(created_by_id__in=user_ids) &
            (Q(is_private=False) | Q(created_by=request.user))
        )
    serializer = PostSerializers(posts, many=True, context={'request': request})

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_detail(request, pk):
    user_ids = [request.user.id] +  [friend.id for friend in request.user.friends.all()]
    post = Post.objects.filter(Q(created_by_id__in=list(user_ids)) or Q(is_private=False)).get(pk=pk)

    return JsonResponse({
        'post': PostDetailSerializer(post).data,

    })


@api_view(['GET'])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)

    if not (request.user in user.friends.all() or request.user == user):
        posts = posts.filter(is_private=False)

    posts_serializer = PostSerializers(posts, many=True)
    user_serializer = UserSerializers(user)

    can_send_friendship_request = True
    if request.user in user.friends.all():
        can_send_friendship_request = False

    existing_request_sent = FriendshipRequest.objects.filter(created_for=user, created_by=request.user).exists()
    existing_request_received = FriendshipRequest.objects.filter(created_for=request.user, created_by=user).exists()
    if existing_request_received or existing_request_sent:
        can_send_friendship_request = False

    return JsonResponse({
        'posts': posts_serializer.data,
        'user': user_serializer.data,
        'can_send_friendship_request': can_send_friendship_request,
    }, safe=False)


@api_view(['POST'])
def post_create(request):
    form = PostForm(request.POST)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)

    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        if attachment:
            post.attachments.add(attachment)

        user = request.user
        user.posts_count = user.posts_count + 1
        user.save()

        serializer = PostSerializers(post)

        return JsonResponse(serializer.data, safe=False)
    else:

        return JsonResponse({'error': 'add something here later!'})


@api_view(['DELETE'])
def post_delete(request, pk):
    post = Post.objects.filter(created_by=request.user).get(pk=pk)
    post.delete()

    return JsonResponse({'message': 'post deleted'})


@api_view(['POST'])
def post_report(request, pk):
    post = Post.objects.get(pk=pk)
    post.reported_by_users.add(request.user)
    post.save()
    return JsonResponse({'message': 'post reported'})


@api_view(['POST'])
def post_like(request, pk):
    post = Post.objects.get(pk=pk)
    like = Like.objects.filter(created_by=request.user, post=post).first()
    if like:
        like.delete()
        post = Post.objects.get(pk=pk)

        post.likes_count = post.likes_count - 1
        post.likes.remove(like)
        post.save()
        return JsonResponse({'message': 'dislike created'})

    else:
        like = Like.objects.create(created_by=request.user)
        post = Post.objects.get(pk=pk)

        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()
        notification = create_notification(request, 'post_like', post_id=post.id)
        return JsonResponse({'message': 'like created'})


@api_view(['POST'])
def post_create_comment(request, pk):
    comment = Comment.objects.create(body=request.data.get('body'), created_by=request.user)

    post = Post.objects.get(pk=pk)
    post.comments_count = post.comments_count + 1
    post.comments.add(comment)
    post.save()

    notification = create_notification(request, 'post_comment', post_id=post.id)

    serializer = CommentSerializer(comment)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def get_trends(request):
    serializer = TrendSerializer(Trend.objects.all(), many=True)
    return JsonResponse(serializer.data, safe=False)
