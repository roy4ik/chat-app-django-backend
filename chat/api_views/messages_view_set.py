from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from chat.models import Message, Conversation


# messages view sets
# from chat.permissions import get_permissions


class MessageViewSet(ModelViewSet):

    def list(self, request, pk=None, **kwargs):
        # list all messages created by the user or with the user as receiver
        queryset = Message.objects.filter(conversation=Conversation.objects.get(participants__in=[request.user]))
        serializer = self.get_serializer(many=True)

    def retrieve(self, request, message_pk=None, *args, **kwargs):
        """retrieves a specific message for a user"""
        # permissions = get_permissions()
        if message_pk:
            message = Message.objects.get(id=message_pk)
        else:
            message = Message.objects.fileter(id=message_pk).last()
        pass

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            #  add serializer class for Update
            pass

    @staticmethod
    def set_message_read(message, reader):
        message.recipients.get(recipient=reader).set_read()
        return message
