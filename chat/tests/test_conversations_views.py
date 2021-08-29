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
        url = reverse('Conversation-list')
        request = requests_factory.get(url, format='json')
        view = ConversationViewSet.as_view({"get": "retrieve"})
        force_authenticate(request, user=conversation.created_by, token=conversation.created_by.auth_token)
        response = view(request, pk=conversation.id)
        serializer = ConversationSerializer(conversation)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_conversation(self):
        url = reverse('Conversation-list')
        request = requests_factory.get(url, format='json')
        view = ConversationViewSet.as_view({"get": "retrieve"})
        force_authenticate(request, user=self.sender, token=self.sender.auth_token)
        response = view(request, pk=Conversation.objects.all().count())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateConversationTest(ConversationTestBase):
    def test_create_valid_conversation(self):
        url = reverse('Conversation-list')
        data = {
            "name": "New Conversation",
            "participants": [self.recipient.id],
        }
        request = requests_factory.post(url, format='json', data=data)
        view = ConversationViewSet.as_view({"post": "create"})
        force_authenticate(request, user=self.sender, token=self.sender.auth_token)
        response = view(request, kwargs=data)
        # serializer = ConversationSerializer(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(response.data, serializer.data)

    def test_create_invalid_conversation(self):
        url = reverse('Conversation-list')
        request = requests_factory.post(url, format='json')
        view = ConversationViewSet.as_view({"post": "create"})
        force_authenticate(request, user=self.sender, token=self.sender.auth_token)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateConversationTest(ConversationTestBase):
    def test_update_valid_conversation(self):
        conversation = self.setUpConversation()
        url = reverse('Conversation-list')
        data = {
            "name": "New Conversation",
            "participants": [self.recipient.id],
        }
        request = requests_factory.put(url, format='json', data=data)
        view = ConversationViewSet.as_view({"put": "update"})
        force_authenticate(request, user=self.sender, token=self.sender.auth_token)
        response = view(request, pk=conversation.id, kwargs=data)
        # serializer = ConversationSerializer(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data, serializer.data)

    def test_update_invalid_conversation(self):
        conversation = self.setUpConversation()
        url = reverse('Conversation-list')
        request = requests_factory.put(url, format='json')
        view = ConversationViewSet.as_view({"put": "update"})
        force_authenticate(request, user=self.sender, token=self.sender.auth_token)
        response = view(request, pk=conversation.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteConversationTest(ConversationTestBase):
    def test_delete_valid_conversation(self):
        conversation = self.setUpConversation()
        url = reverse('Conversation-list')
        data = {
            "name": "New Conversation",
            "participants": [self.recipient.id],
        }
        request = requests_factory.put(url, format='json', data=data)
        view = ConversationViewSet.as_view({"put": "destroy"})
        force_authenticate(request, user=self.sender, token=self.sender.auth_token)
        response = view(request, pk=conversation.id, kwargs=data)
        # serializer = ConversationSerializer(response)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # self.assertEqual(response.data, serializer.data)

    def test_delete_invalid_conversation(self):
        url = reverse('Conversation-list')
        request = requests_factory.put(url, format='json')
        view = ConversationViewSet.as_view({"put": "destroy"})
        force_authenticate(request, user=self.sender, token=self.sender.auth_token)
        response = view(request, pk=Conversation.objects.all().count()+1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
