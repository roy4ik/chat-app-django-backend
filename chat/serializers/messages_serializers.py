from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import serializers

from chat.models import Message, Conversation
from chat.serializers.recipient_serializers import RecipientSerializer
from chat.serializers.user_serializer import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    conversation_id = serializers.IntegerField(required=True)
    content = serializers.CharField(max_length=1024)
    created_by = UserSerializer(many=False, required=False,
                                read_only=True)
    recipients = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'id',
            'created_by',
            'conversation_id',
            'date_created',
            'date_updated',
            'subject',
            'content',
            'recipients',
        ]
        read_only_fields = [
            'id',
            'created_by',
        ]
        depth = 2

    def _recipient_data_to_internal(self):
        recipients = self.context.get('request').data.get('recipients')
        self.validate_recipients(recipients)
        try:
            recipient_objects = User.objects.filter(id__in=recipients).\
                exclude(id=self.context.get('request').user.id).all()
            if recipient_objects:
                return recipient_objects
            else:
                raise ObjectDoesNotExist()
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Recipient Users are not valid or cannot be found! "
                                              "Note that only users that are not the creator of a message can "
                                              "be recipients of the same message")


    @staticmethod
    def validate_recipients(recipients):
        if type(recipients) == list:
            for recipient in recipients:
                if not type(recipient) == int:
                    raise serializers.ValidationError(
                        {'detail': f"Validation for recipient failed: expects a list of "
                                   f"ints for participants"})
        else:
            raise serializers.ValidationError({'detail': f"Validation for recipient failed: expects a list of "
                                                         f"ints for participants -> got {recipients}"})

    def create(self, validated_data) -> Message:
        conversation_id = validated_data.get('conversation_id')
        if not conversation_id:
            raise serializers.ValidationError({'detail': "Conversation_id is required to create a message"})
        with transaction.atomic():
            try:
                recipients = self._recipient_data_to_internal()
                user = self.context.get('request').user
                conversation = Conversation.objects.get(id=conversation_id)
                message = Message(created_by=user,
                                  conversation=conversation,
                                  subject=validated_data.get('subject'),
                                  content=validated_data.get('content'),
                                  recipients=recipients)
                message.save()
            except ObjectDoesNotExist as e:
                raise serializers.ValidationError({'detail': e})

            return message

    @staticmethod
    def get_recipients(obj):
        return [RecipientSerializer(recipient).data for recipient in obj.recipient_set.all()]
