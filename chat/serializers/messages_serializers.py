from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import serializers

from chat.models import Message, Recipient, Conversation
from chat.serializers.recipient_serializers import RecipientSerializer


class MessageSerializer(serializers.ModelSerializer):
    conversation_id = serializers.IntegerField(required=True)
    content = serializers.CharField(max_length=1024)
    recipients = RecipientSerializer(many=True, required=False)

    class Meta:
        model = Message
        fields = [
            'id',
            'conversation_id',
            'date_created',
            'date_updated',
            'created_by',
            'subject',
            'content',
            'recipients',
        ]
        depth = 5

    def create(self, validated_data) -> Message:
        conversation_id = validated_data.get('conversation_id')
        if not conversation_id:
            raise serializers.ValidationError({'detail': "Conversation_id is required to create a message"})

        with transaction.atomic():
            try:
                user = self.context.get('request').user
                conversation = Conversation.objects.get(id=conversation_id)
                message = Message(created_by=user,
                                  conversation=conversation,
                                  subject=validated_data.get('subject'),
                                  content=validated_data.get('content'))
            except ObjectDoesNotExist:
                raise serializers.ValidationError({'detail': 'conversation does not exist'})

            return message

    def update(self, instance, validated_data) -> Message:
        super().update(instance, validated_data)
        with transaction.atomic():
            instance.date_updated = datetime.utcnow()
            instance.save()
        return instance


