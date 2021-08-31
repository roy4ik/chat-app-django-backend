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


class GetConversationListTest(ConversationTestBase):
    serializer = ConversationSerializer

    def test_get_valid_conversation_list(self):
        conversations = [self.setUpConversation() for conversation in range(5)]
        response = self.return_viewset_response(
            url=reverse('Conversation-list'),
            data=None,
            viewset_class=ConversationViewSet,
            method='get',
            action='list',
            auth_user=self.sender)
        serializer = self.serializer(conversations, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, serializer.data)

    def test_get_invalid_conversation_list(self):
        response = self.return_viewset_response(
            url=reverse('Conversation-list'),
            data=None,
            viewset_class=ConversationViewSet,
            method='get',
            action='list',
            auth_user=self.sender)
        self.assertListEqual([], response.data)

    def test_get_forbidden_conversation_list(self):
        conversations = [self.setUpConversation() for conversation in range(5)]
        response = self.return_viewset_response(
            url=reverse('Conversation-list'),
            data=None,
            viewset_class=ConversationViewSet,
            method='get',
            action='list',
            auth_user=self.no_access_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, [])


class GetSingleConversationTest(ConversationTestBase):
    serializer = ConversationSerializer

    def test_get_valid_single_conversation(self):
        conversation = self.setUpConversation()
        response = self.return_viewset_response(
            url=reverse('Conversation-list'),
            data=None,
            viewset_class=ConversationViewSet,
            method='get',
            action='retrieve',
            auth_user=self.sender,
            pk=conversation.id)
        serializer = self.serializer(conversation)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_conversation(self):
        response = self.return_viewset_response(
            url=reverse('Conversation-list'),
            data=None,
            viewset_class=ConversationViewSet,
            method='get',
            action='retrieve',
            auth_user=self.sender,
            pk=Conversation.objects.all().count())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_forbidden_single_conversation(self):
        conversation = self.setUpConversation()
        response = self.return_viewset_response(
            url=reverse('Conversation-list'),
            data=None,
            viewset_class=ConversationViewSet,
            method='get',
            action='retrieve',
            auth_user=self.no_access_user,
            pk=conversation.id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateConversationTest(ConversationTestBase):
    # serializer = ConversationSerializer

    def test_create_valid_conversation(self):
        data = {
            "name": "New Conversation",
            "participants": [self.recipient.id],
        }
        response = self.return_viewset_response(
            url=reverse('Conversation-list'),
            data=data,
            viewset_class=ConversationViewSet,
            method='post',
            action='create',
            auth_user=self.sender)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_conversation(self):
        response = self.return_viewset_response(
            url=reverse('Conversation-list'),
            data=None,
            viewset_class=ConversationViewSet,
            method='post',
            action='create',
            auth_user=self.sender)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # no forbidden test for create as every user can create a conversation


class UpdateConversationTest(ConversationTestBase):
    def test_update_valid_conversation(self):
        conversation = self.setUpConversation()
        data = {
            "name": "New Conversation",
            "participants": [self.recipient.id, self.sender.id],
        }
        response = self.return_viewset_response(
            url=reverse('Conversation-list'),
            data=data,
            viewset_class=ConversationViewSet,
            method='put',
            action='update',
            auth_user=self.sender,
            pk=conversation.id)
        serializer = ConversationSerializer(conversation)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, serializer.data)

    def test_update_invalid_conversation(self):
        conversation = self.setUpConversation()
        response = self.return_viewset_response(
            url=reverse('Conversation-list'),
            data=None,
            viewset_class=ConversationViewSet,
            method='put',
            action='update',
            auth_user=self.sender,
            pk=conversation.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_forbidden_conversation(self):
        conversation = self.setUpConversation()
        data = {
            "name": "New Conversation",
            "participants": [self.recipient.id, self.sender.id],
        }
        response = self.return_viewset_response(
            url=reverse('Conversation-list'),
            data=data,
            viewset_class=ConversationViewSet,
            method='put',
            action='update',
            auth_user=self.no_access_user,
            pk=conversation.id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteConversationTest(ConversationTestBase):
    def test_delete_valid_conversation(self):
        conversation = self.setUpConversation()
        data = {
            "name": "New Conversation",
            "participants": [self.recipient.id],
        }
        response = self.return_viewset_response(
            url=reverse('Conversation-list'),
            data=data,
            viewset_class=ConversationViewSet,
            method='delete',
            action='destroy',
            auth_user=self.sender,
            pk=conversation.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_conversation(self):
        response = self.return_viewset_response(
            url=reverse('Conversation-list'),
            data=None,
            viewset_class=ConversationViewSet,
            method='delete',
            action='destroy',
            auth_user=self.sender,
            pk=Conversation.objects.all().count())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_forbidden_conversation(self):
        conversation = self.setUpConversation()
        data = {
            "name": "New Conversation",
            "participants": [self.recipient.id],
        }
        response = self.return_viewset_response(
            url=reverse('Conversation-list'),
            data=data,
            viewset_class=ConversationViewSet,
            method='delete',
            action='destroy',
            auth_user=self.no_access_user,
            pk=conversation.id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
