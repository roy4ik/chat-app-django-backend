from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework.test import force_authenticate
from .conversation_test_helpers import ConversationTestBase
from ..api_views.conversations_view_set import ConversationViewSet
from ..models import Conversation
from ..serializers.conversations_serializers import ConversationSerializer
from rest_framework.test import APIRequestFactory

# initialize the APIClient app
client = APIClient()
requests_factory = APIRequestFactory()


class GetSingleConversationTest(ConversationTestBase):
    def test_get_valid_single_conversation(self):
        conversation = self.setUpConversation()
        url = reverse('Conversation-list') + str(conversation.id) + '/'
        request = requests_factory.get(url, format='json')
        view = ConversationViewSet.as_view({"get": "retrieve"})
        force_authenticate(request, user=conversation.created_by, token=conversation.created_by.auth_token)
        response = view(request, pk=conversation.id)
        serializer = ConversationSerializer(conversation)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_conversation(self):
        pk = Conversation.objects.all().count()
        url = reverse('Conversation-list') + str(pk) + '/'
        request = requests_factory.get(url, format='json')
        view = ConversationViewSet.as_view({"get": "retrieve"})
        force_authenticate(request, user=self.sender, token=self.sender.auth_token)
        response = view(request, pk=pk)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
