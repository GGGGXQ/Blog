from django.contrib import auth

from .models import Post, Like
from rest_framework import serializers
from account.serializers import UserSerializers

class PostSerializers(serializers.ModelSerializer):
    created_by = UserSerializers(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'body', 'likes_count', 'is_liked', 'created_by', 'created_at_formatted']
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if not request:
            return False

        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return False  

        return Like.objects.filter(post=obj, created_by=user).exists()
