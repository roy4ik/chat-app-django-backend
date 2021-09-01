from django.db.models import Q
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from chat.models import Conversation
from chat.serializers.conversations_serializers import ConversationSerializer
from rest_framework.decorators import action
from django.db.models import QuerySet


class ConversationViewSet(ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def list(self, request, **kwargs) -> Response:
        """Returns all the user's conversation including where he only participates."""
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='owned')
    def list_owned_conversations(self, request, **kwargs) -> Response:
        """Returns all the user's conversations that he created/owns."""
        queryset = Conversation.objects.filter(created_by=self.request.user).distinct()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self) -> QuerySet:
        if self.request.method == 'GET':
            # get all conversations that the user participates in.
            # note: this is only for get methods as this includes other user's conversations
            if self.action == 'retrieve':
                return Conversation.objects.filter(Q(created_by=self.request.user)
                                            | Q(participants__exact=self.request.user),
                                            pk=self.kwargs.get('pk')).distinct()
            return Conversation.objects.filter(Q(created_by=self.request.user)
                                               | Q(participants__exact=self.request.user)).distinct()
        else:
            pk = self.kwargs.get('pk')
            return Conversation.objects.filter(created_by=self.request.user, pk=pk).distinct()
