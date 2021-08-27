from django.db import transaction
from rest_framework.authtoken.admin import User
from django.test import TestCase
from chat.models import Message, Conversation


class ConversationTestBase(TestCase):

    def setUp(self):
        # create conversation
        self.sender = User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret')
        self.recipient = User.objects.create_user(
            username='mark', email='mark@gmail.com', password='super_top_secret')

    def setUp_message(self, conversation, subject, content, flip_sender_recipient=False):
        if flip_sender_recipient:
            tmp = self.sender
            self.sender = self.recipient
            self.recipient = tmp
            # adding participants
            with transaction.atomic():
                conversation.participants.add(self.recipient)
                conversation.save()

                message = Message(
                    conversation=conversation,
                    created_by=self.sender,
                    subject=subject,
                    content=content)
                message.save()

            return message

    def setUpConversation(self):
        with transaction.atomic():
            # create conversation
            conversation = Conversation.objects.create(
                name="Test",
                created_by=self.sender)
            return conversation

    def setUp_conversation_with_messages(self, n_messages=5):
        conversation = self.setUpConversation()
        for n in range(n_messages):
            subject = 'TEST MESSAGE' + str(n)
            content = "Test message for conversation test" + str(n)
            self.setUp_message(conversation,
                               subject=subject,
                               content=content,
                               flip_sender_recipient=True)
        return conversation


    @staticmethod
    def set_message_read(message, reader):
        message.recipients.get(recipient=reader).set_read()
        return message

    @staticmethod
    def assert_message_read(message, reader):
        message.recipients.get(recipient=reader).set_read()
        return message

    def mark__conversation_read(self, conversation, reader):
        messages = Message.objects.filter(conversation=conversation,
                                          recipients__recipient__exact=reader)
        read_messages = [self.set_message_read(message, reader) for message in messages]
        [self.assert_message_read(message, reader) for message in messages]

