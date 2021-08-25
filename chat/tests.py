from django.test import TransactionTestCase
from django.db import transaction
from chat.models import Conversation, Message
from accounts.models import User


# Create your tests here.
class ConversationTestCase(TransactionTestCase):
    def setUp(self):
        # create conversation
        self.sender = User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret')
        self.recipient = User.objects.create_user(
            username='mark', email='mark@gmail.com', password='super_top_secret')

    def setUp_conversation_with_message(self):
        with transaction.atomic():
            # create conversation
            conversation = Conversation.objects.create(
                created_by=self.sender)
            # adding participants
            conversation.participants.add(self.recipient)
            conversation.save()

            message = Message(
                conversation=conversation,
                created_by=self.sender,
                subject='TEST MESSAGE',
                content="Test message for conversation test.")
            message.save()

            return conversation, message

    def test_conversation(self):
        conversation, message = self.setUp_conversation_with_message()
        assert conversation
        assert message

    def test_message_read(self, read=False):
        conversation, message = self.setUp_conversation_with_message()
        with transaction.atomic():
            for recipient in conversation.participants.all():
                read_status = message.read_statuses.get(recipient=recipient)
                if read:
                    assert read_status.set_read()
                    read_status.save()

