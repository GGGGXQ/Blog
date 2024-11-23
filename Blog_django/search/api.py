from re import U
from django.http import JsonResponse, QueryDict
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from account.serializers import UserSerializers

from post.models import Post
from post.serializers import PostSerializers


@api_view(['POST'])
def search(request):
    data = request.data
    query = data['query']
    
    users = User.objects.filter(name__icontains=query)
    user_serializer = UserSerializers(users, many=True)

    posts = Post.objects.filter(body__icontains=query)
    post_serializer = PostSerializers(posts, many=True)

    return JsonResponse({
        'users': user_serializer.data,
        'posts': post_serializer.data, 
    }, safe=False)