from django.contrib.auth.models import User
from rest_framework import serializers
from chat.serializers.user_serializer import UserSerializer
from chat.models import Recipient


class RecipientSerializer(serializers.ModelSerializer):
    recipient_user = UserSerializer(read_only=True)
    date_read = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Recipient
        fields = [
            'recipient_user',
            'date_read',
        ]
