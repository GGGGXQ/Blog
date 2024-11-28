from rest_framework import serializers

from account.serializers import UserSerializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    created_for_id = serializers.PrimaryKeyRelatedField(source='created_for', read_only=True)
    class Meta:
        model = Notification
        fields = ('id', 'body', 'type_of_notification', 'post_id', 'created_for_id')