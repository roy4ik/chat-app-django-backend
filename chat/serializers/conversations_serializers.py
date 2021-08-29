from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import serializers
from chat.models import Conversation
from chat.serializers.user_serializer import UserSerializer


class ConversationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=128)
    created_by = UserSerializer(many=False, required=False)

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

    def create(self, validated_data):
        participants_data = validated_data.get('participants')
        if not participants_data:
            raise ValueError("Participants are required to create a conversation")

        with transaction.atomic():
            user = self.context.get('request').user
            conversation = Conversation.objects.create(created_by=user)
            conversation.save()
            # .objects.create(user=user, **profile_data)
            for participant_user in participants_data:
                try:
                    conversation.participants.add(participant_user)
                except ObjectDoesNotExist:
                    raise serializers.ValidationError({'detail': 'participant does not exist'})

            return conversation
