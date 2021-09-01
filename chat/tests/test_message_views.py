from rest_framework.reverse import reverse
from rest_framework import status
from .conversation_test_helpers import ConversationTestBase
from ..api_views.messages_view_set import MessageViewSet
from ..models import Conversation
from ..serializers.messages_serializers import MessageSerializer


class ReadSingleMessage(ConversationTestBase):
    serializer = MessageSerializer

    def test_read_valid_single_message(self):
        conversation, messages = self.setUp_conversation_with_messages()
        response = self.return_viewset_response(
            url=reverse('Message-list'),
            data=None,
            viewset_class=MessageViewSet,
            method='get',
            action='read',
            auth_user=conversation.created_by,
            pk=messages[0].id)
        serializer = self.serializer(messages[0])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert [recipient for recipient in response.data.get('recipients')
                if recipient.get('date_read')
                and recipient.get('recipient_user').get('id') == conversation.created_by.id]
        self.assertEqual(response.data, serializer.data)

    def test_read_invalid_single_message(self):
        conversation, messages = self.setUp_conversation_with_messages()
        response = self.return_viewset_response(
            url=reverse('Message-list'),
            data=None,
            viewset_class=MessageViewSet,
            method='get',
            action='read',
            auth_user=conversation.created_by,
            pk=messages[-1].id + 1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_valid_single_message(self):
        conversation, messages = self.setUp_conversation_with_messages()
        response = self.return_viewset_response(
            url=reverse('Message-list'),
            data=None,
            viewset_class=MessageViewSet,
            method='get',
            action='retrieve',
            auth_user=conversation.created_by,
            pk=messages[0].id)
        serializer = self.serializer(messages[0])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_message(self):
        conversation, messages = self.setUp_conversation_with_messages()
        response = self.return_viewset_response(
            url=reverse('Message-list'),
            data=None,
            viewset_class=MessageViewSet,
            method='get',
            action='retrieve',
            auth_user=conversation.created_by,
            pk=messages[-1].id + 1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateMessageTest(ConversationTestBase):
    serializer = MessageSerializer

    def test_create_valid_message(self):
        conversation = self.setUpConversation()
        data = {
            "conversation_id": conversation.id,
            "subject": "New Subject",
            "content": "This is a new message"
        }
        response = self.return_viewset_response(
            url=reverse('Message-list'),
            data=data,
            viewset_class=MessageViewSet,
            method='post',
            action='create',
            auth_user=conversation.created_by)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_message(self):
        data = {
            "conversation_id": Conversation.objects.all().count() + 1,
            "subject": "New Subject",
            "content": "This is a new message"
        }
        response = self.return_viewset_response(
            url=reverse('Message-list'),
            data=data,
            viewset_class=MessageViewSet,
            method='post',
            action='create',
            auth_user=self.sender)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
