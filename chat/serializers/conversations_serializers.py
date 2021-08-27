from rest_framework import serializers
# conversation serializers
from chat.models import Conversation
from chat.serializers.user_serializer import UserSerializer

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)
    created_by = UserSerializer(many=False)

    class Meta:
        model = Conversation
        fields = [
            'id',
            'name',
            'created_by',
            'participants'
        ]
        read_only_fields = [
            'id',
        ]
