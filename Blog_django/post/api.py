from json import JSONDecodeError
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .forms import PostForm
from .models import Post, Like, Comment, Trend
from .serializers import CommentSerializer, PostSerializers, PostDetailSerializer, TrendSerializer
from account.models import User
from account.serializers import UserSerializers


@api_view(['GET'])
def post_list(request):
    user_ids = [request.user.id] +  [friend.id for friend in request.user.friends.all()]
    posts = Post.objects.filter(created_by_id__in=list(user_ids))
    trend = request.GET.get('trend', '')

    if trend:
        posts = posts.filter(body__icontains='#' + trend)
    serializer = PostSerializers(posts, many=True, context={'request': request})

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)

    return JsonResponse({
        'post': PostDetailSerializer(post).data,
        
    })


@api_view(['GET'])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)

    post_serializer = PostSerializers(posts, many=True, context={'request': request})

    user_serializer = UserSerializers(user)

    return JsonResponse({
        'posts':post_serializer.data, 
        'user': user_serializer.data,
    }, safe=False)


@api_view(['POST'])
def post_create(request):
    form = PostForm(request.data)

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        user = request.user
        user.posts_count = user.posts_count + 1
        user.save()

        serializer = PostSerializers(post)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add something here later!'})
    

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
        return JsonResponse({'message': 'like created'})


@api_view(['POST'])
def post_create_comment(request, pk):
    comment = Comment.objects.create(body=request.data.get('body'), created_by=request.user)

    post = Post.objects.get(pk=pk)
    post.comments_count = post.comments_count + 1
    post.comments.add(comment)
    post.save()
    
    serializer = CommentSerializer(comment)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def get_trends(request):
    serializer = TrendSerializer(Trend.objects.all(), many=True)
    return JsonResponse(serializer.data, safe=False)
