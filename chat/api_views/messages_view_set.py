from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from chat.models import Message
from chat.serializers.messages_serializers import MessageSerializer
from django.db.models import QuerySet


class MessageViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def list(self, request, conversation_id=None, **kwargs) -> Response:
        """Lists all messages created by the user or with the user as receiver."""
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='/list_unread')
    def list_unread(self, request, **kwargs) -> Response:
        """Lists all unread messages created by the user or with the user as recipient."""
        queryset = Message.objects.filter(
            recipients__recipient_user=[request.user],
            recipient__date_read=not None)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs) -> Response:
        """Retrieves a specific message for a user."""
        try:
            serializer = self.serializer_class(self.get_queryset())
            return Response(serializer.data)
        except Message.DoesNotExist:
            return Response(status=404)

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated], url_path='/read')
    def read(self, request, *args, **kwargs) -> Response:
        """
        Marks a specific message for a user  as read.
        note: Only recipients of a message can mark it read for themselves.
        """
        try:
            queryset = Message.objects.get(recipients__recipient_user=request.user,
                                           pk=kwargs.get('pk'))
            self.set_read(queryset, request.user)
            serializer = self.serializer_class(queryset)
            return Response(serializer.data)
        except Message.DoesNotExist:
            return Response(status=404)

    def delete(self, request, *args, **kwargs):
        """
        Deletes a message.
        note: A user can only delete a message if he is an owner or recipient of the message
        """
        try:
            queryset = Message.objects.get((Q(created_by=self.request.user)
                                            | Q(recipients__recipient_user=self.request.user)),
                                           pk=self.kwargs.get('pk'))
            serializer = self.serializer_class(queryset)

            return Response(serializer.data)
        except Message.DoesNotExist:
            return Response(status=404)

    @staticmethod
    def set_read(message, reader) -> Message:
        """
        Sets a message as read
        Args:
            message (Message): message object
            reader (User): user object
        Returns:
            message
        """
        message.recipients.get(recipient_user=reader).set_read()
        return message

    def get_queryset(self) -> QuerySet:
        if self.request.method == 'GET':
            if self.action == 'retrieve':
                return Message.objects.get((Q(created_by=self.request.user)
                                            | Q(recipients__recipient_user=self.request.user)),
                                           pk=self.kwargs.get('pk'))
            else:
                return Message.objects.filter(Q(created_by=self.request.user)
                                              | Q(recipients__recipient_user=self.request.user))
        else:
            return Message.objects.filter((Q(created_by=self.request.user)
                                           | Q(recipients__recipient_user=self.request.user)),
                                          pk=self.kwargs.get('pk'))
