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
            conversation, message = self.setUp_conversation_with_messages()
            assert conversation
            assert message

    def test_message_read(self, read=True, reader=None):
        if not reader:
            reader = self.recipient
        conversation = self.setUp_conversation_with_messages()
        messages = Message.objects.filter(conversation=conversation,
                                          recipients__recipient__exact=reader)
        for message in messages:
            recipient = message.recipients.get(recipient=reader)
            if read:
                assert recipient.set_read()

    def test_retrieve_all_user_conversations_messages(self):
        user = self.sender
        conversation1 = self.setUp_conversation_with_messages()
        conversation2 = self.setUp_conversation_with_messages()
        conversation3 = self.setUp_conversation_with_messages()
        q_conversations = Conversation.objects.filter(Q(created_by=user) | Q(participants__exact=user)).distinct()
        assert ([conversation.id for conversation in q_conversations.all()] == [conversation1.id, conversation2.id,
                                                                                conversation3.id])
        # messages = Message.objects.filter(conversation__in=q_conversations)
        messages = Message.objects.filter(conversation__in=q_conversations).prefetch_related()

    def test_retrieve_all_user_created_messages(self):
        user = self.sender
        conversation = self.setUp_conversation_with_messages()
        conversation2 = self.setUp_conversation_with_messages()
        conversation3 = self.setUp_conversation_with_messages()
        messages = Message.objects.filter(created_by=self.sender)

    def test_retrieve_all_user_received_unread(self):
        user = self.sender
        conversation = self.setUp_conversation_with_messages()
        conversation2 = self.setUp_conversation_with_messages()
        conversation3 = self.setUp_conversation_with_messages()
        messages = Message.objects.filter(recipients__recipient__exact=user)
        for message in messages:
            for recipient in message.recipients.all():
                assert not recipient.is_read()
