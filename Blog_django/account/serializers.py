from ast import main
from .models import User, FriendshipRequest
from rest_framework import serializers


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'friends_count']


class FriendshipRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializers(read_only=True)

    class Meta:
        model = FriendshipRequest
        fields = ['id', 'created_by']
