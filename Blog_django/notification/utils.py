from account.models import FriendshipRequest
from .models import Notification
from post.models import Post

# create_notification(request, 'post_like', 'kfsk-23m232131-jsj-fsaf', 'kfsk-23m232131-jsj-fsaf')

def create_notification(request, type_of_notification, post_id=None, friendrequest_id=None):
    created_for = None

    if type_of_notification == 'post_like':
        body = f'{request.user.name} 赞了你'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by
    elif type_of_notification == 'post_comment':
        body = f'{request.user.name} 评论了你'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by
    elif type_of_notification == 'new_friendrequest':
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
        body = f'{request.user.name} 请求加你为好友'
    elif type_of_notification == 'accepted_friendrequest':
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
        body = f'{request.user.name} 通过了你的好友申请'
    elif type_of_notification == 'rejected_friendrequest':
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
        body = f'{request.user.name} 拒绝了你的好友申请'



    notification =Notification.objects.create(
        body = body,
        type_of_notification = type_of_notification, 
        post_id=post_id,
        created_by = request.user, 
        created_for=created_for
    )
    
    return notification