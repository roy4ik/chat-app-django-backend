from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from chat.models import Message

from chat.serializers.messages_serializers import MessageSerializer


class MessageViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def list(self, request, conversation_id=None, **kwargs) -> Response:
        """lists all messages created by the user or with the user as receiver"""
        if not conversation_id:
            pass
        queryset = Message.objects.filter(Q(created_by=request.user)
                                          | Q(recipients__recipient_user=request.user))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='/list_unread')
    def list_unread(self, request, **kwargs) -> Response:
        """lists all unread messages created by the user or with the user as receiver"""
        queryset = Message.objects.filter(
            recipients__recipient_user=[request.user],
            recipient__date_read=not None)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs) -> Response:
        """retrieves a specific message for a user"""
        try:
            queryset = Message.objects.get((Q(created_by=request.user)
                                            | Q(recipients__recipient_user=request.user)),
                                           pk=kwargs.get('pk'))
            serializer = self.serializer_class(queryset)
            return Response(serializer.data)
        except Message.DoesNotExist:
            return Response(status=404)

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated], url_path='/read')
    def read(self, request, *args, **kwargs) -> Response:
        """marks a specific message for a user  as read"""
        # permissions = get_permissions()
        try:
            queryset = Message.objects.get((Q(created_by=request.user)
                                            | Q(recipients__recipient_user=request.user)),
                                           pk=kwargs.get('pk'))
            self.set_read(queryset, request.user)
            serializer = self.serializer_class(queryset)

            return Response(serializer.data)
        except Message.DoesNotExist:
            return Response(status=404)

    @staticmethod
    def set_read(message, reader) -> Message:
        """
        sets a message as read
        Args:
            message (Message): message object
            reader (User): user object
        Returns:
            message
        """
        message.recipients.get(recipient_user=reader).set_read()
        return message
