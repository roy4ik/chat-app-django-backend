from rest_framework import serializers
from chat.serializers.user_serializer import UserSerializer
from chat.models import Recipient


class RecipientSerializer(serializers.ModelSerializer):
    recipient_user = UserSerializer(many=False, required=False)

    class Meta:
        model = Recipient
        fields = [
            'id',
            'date_read',
            'recipient_user',
        ]
        depth = 1
