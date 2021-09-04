from django.db.models import Q
from chat.models import Conversation, Message

# Create your tests here.
from chat.tests.conversation_test_helpers import ConversationTestBase


class ConversationTestCase(ConversationTestBase):
    def test_create_conversation(self, n_messages=5):
        if n_messages:
            conversation = self.setUpConversation()
            assert conversation
        else:
            conversation, messages = self.setUp_conversation_with_messages()
            assert conversation
            assert messages

    def test_message_read(self, read=True, reader=None):
        if not reader:
            reader = self.recipient
        conversation, messages = self.setUp_conversation_with_messages()
        messages = Message.objects.filter(conversation=conversation, recipients=reader)
        for message in messages:
            recipient = message.recipient_set.filter(recipient_user=reader).first()
            if read and recipient:
                assert recipient.set_read()

    def test_retrieve_all_user_conversations_messages(self, n_conversations=3):
        user = self.sender
        conversations_list = []
        messages_lists = []
        for conv in range(n_conversations):
            conversation, messages = self.setUp_conversation_with_messages()
            conversations_list.append(conversation)
            messages_lists.append(messages)
        q_conversations = Conversation.objects.filter(Q(created_by=user) |
                                                      Q(messages__recipients=user)).distinct()
        assert [conv for conv in q_conversations.all()] == conversations_list
        # messages = Message.objects.filter(conversation__in=q_conversations)
        messages_by_user = []
        [[messages_by_user.append(message) for message in conversation]
         for conversation in messages_lists]
        assert [message for message in messages_lists for messages_list in messages_lists]

    def test_retrieve_all_user_created_messages(self, n_conversations=3):
        user = self.sender
        conversations_list = []
        messages_lists = []
        for conv in range(n_conversations):
            conversation, messages = self.setUp_conversation_with_messages()
            conversations_list.append(conversation)
            messages_lists.append(messages)
        messages_query = [m for m in Message.objects.filter(
            created_by=user)]
        messages_by_user = []
        [[messages_by_user.append(message) for message in conversation
          if message.created_by == user]
         for conversation in messages_lists]
        assert messages_by_user == messages_query

    def test_retrieve_all_user_received_unread(self, n_conversations=3):
        user = self.sender
        conversations_list = []
        messages_lists = []
        for conv in range(n_conversations):
            conversation, messages = self.setUp_conversation_with_messages()
            conversations_list.append(conversation)
            messages_lists.append(messages)
        messages = Message.objects.filter(recipients=user)
        for message in messages:
            for recipient in message.recipient_set.all():
                assert not recipient.is_read()
