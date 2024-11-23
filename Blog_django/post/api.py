import re
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import PostForm
from .models import Post
from .serializers import PostSerializers
from account.models import User
from account.serializers import UserSerializers


@api_view(['GET'])
def post_list(request):
    user_ids = [request.user.id]
    for user in  request.user.friends.all():
        user_ids.append(user.id)
    
    posts = Post.objects.filter(created_by_id__in=list(user_ids))

    serializer = PostSerializers(posts, many=True)

    return JsonResponse(serializer.data, safe=False)



@api_view(['GET'])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)

    post_serializer = PostSerializers(posts, many=True)
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

        serializer = PostSerializers(post)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add something here later!'})