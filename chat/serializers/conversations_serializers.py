from django.db import transaction
from rest_framework import serializers
from chat.models import Conversation
from chat.serializers.user_serializer import UserSerializer


class ConversationSerializer(serializers.ModelSerializer):
    """Serializers Conversations"""
    name = serializers.CharField(max_length=128)
    created_by = UserSerializer(many=False, required=False,
                                read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'id',
            'name',
            'created_by',
            'date_created',
            'date_updated',
        ]
        read_only_fields = [
            'id',
            'created_by',
            'date_created',
        ]

    def create(self, validated_data) -> Conversation:
        """creates an instance with participants"""
        with transaction.atomic():
            user = self.context.get('request').user
            conversation = Conversation.objects.create(name=validated_data.get('name'), created_by=user)
            conversation.save()
            return conversation
