from .models import Post
from rest_framework import serializers
from account.serializers import UserSerializers

class PostSerializers(serializers.ModelSerializer):
    created_by = UserSerializers(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'body', 'created_by', 'created_at_formatted']
        