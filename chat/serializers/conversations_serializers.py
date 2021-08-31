from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import serializers
from chat.models import Conversation
from chat.serializers.user_serializer import UserSerializer


class ConversationSerializer(serializers.ModelSerializer):
    """Serializers Conversations"""
    name = serializers.CharField(max_length=128)
    created_by = UserSerializer(many=False, required=False)

    class Meta:
        model = Conversation
        fields = [
            'id',
            'name',
            'created_by',
            'date_created',
            'participants'
        ]
        read_only_fields = [
            'id',
            'created_by',
            'date_created',
        ]

    def create(self, validated_data) -> Conversation:
        """creates an instance with participants"""
        participants_data = validated_data.get('participants')
        if not participants_data:
            raise serializers.ValidationError({'detail': "Participants are required to create a conversation"})

        with transaction.atomic():
            user = self.context.get('request').user
            conversation = Conversation.objects.create(created_by=user)
            conversation.save()
            for participant_user in participants_data:
                try:
                    conversation.participants.add(participant_user)
                except ObjectDoesNotExist:
                    raise serializers.ValidationError({'detail': 'participant does not exist'})

            return conversation

    def update(self, instance, validated_data) -> Conversation:
        """updates an instance and its date_updated"""
        participants_data = validated_data.get('participants')
        super().update(instance, validated_data)
        with transaction.atomic():
            instance.date_updated = datetime.utcnow()
            instance.save()
        # add new_participants
        try:
            [instance.participants.add(User.objects.get(pk=participant))
             for participant in participants_data
             if participant not in instance.participants.all().only('pk')]
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'detail': 'participant does not exist'})
        return instance
