from rest_framework import serializers
from account.serializers import UserSerializers

from .models import Conversation, ConversationMessage


class ConversationSerializer(serializers.ModelSerializer):
    users = UserSerializers(read_only=True, many=True)
    class Meta:
        model = Conversation
        fields = ['id', 'users', 'modified_at_formatted']


class ConversationMessageSerializer(serializers.ModelSerializer):
    sent_to = UserSerializers(read_only=True)
    created_by = UserSerializers(read_only=True)

    class Meta:
        model = ConversationMessage
        fields = ['id', 'sent_to', 'created_by', 'created_at_formatted', 'body']


class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = ConversationMessageSerializer(read_only=True, many=True)

    class Meta:
        model = Conversation
        fields = ['id', 'users', 'modified_at_formatted', 'messages']
