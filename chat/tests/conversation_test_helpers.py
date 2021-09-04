from django.db import transaction
from rest_framework.authtoken.admin import User
from django.test import TestCase
from chat.models import Message, Conversation
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient

# initialize the APIClient app
client = APIClient()
requests_factory = APIRequestFactory()


class ConversationTestBase(TestCase):

    def setUp(self):
        # create conversation
        self.sender = User.objects.create_user(
            username='jacob', first_name="jacob", last_name="Jacobs", email='jacob@gmail.com', password='top_secret')
        self.recipient = User.objects.create_user(
            username='mark', first_name="mark", last_name="Marks", email='mark@gmail.com', password='super_top_secret')
        self.no_access_user = User.objects.create_user(
            username='noaccess', first_name="noaccess", last_name="noaccess", email='noaccess@gmail.com',
            password='super_top_secret')

    def setUp_message(self, conversation, subject, content, sender, recipients):
        with transaction.atomic():
            message = Message(
                conversation=conversation,
                created_by=sender,
                subject=subject,
                content=content, recipients=recipients)
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
        messages = []
        for n in range(n_messages):
            subject = 'TEST MESSAGE' + str(n)
            content = "Test message for conversation test" + str(n)
            recipients = [self.recipient]
            if n % 2 != 0:
                recipients = [self.sender]
            messages.append(self.setUp_message(conversation,
                                               subject=subject,
                                               content=content,
                                               sender=self.sender,
                                               recipients=recipients))
        return conversation, messages

    @staticmethod
    def set_message_read(message, reader):
        message.recipients.get(recipient_user=reader).set_read()
        return message

    @staticmethod
    def assert_message_read(message, reader):
        assert message.recipients.get(recipient_user=reader).set_read()

    def mark__conversation_read(self, conversation, reader):
        messages = Message.objects.filter(conversation=conversation,
                                          recipients=reader)
        read_messages = [self.set_message_read(message, reader) for message in messages]
        [self.assert_message_read(message, reader) for message in read_messages]

    @staticmethod
    def return_viewset_response(url, data, viewset_class, method, action, auth_user, pk=None):
        """sets up conversation view with force authenticate"""
        if method.upper() == 'DELETE':
            request = requests_factory.delete(url, format='json', data=data)
        elif method.upper() == 'POST':
            request = requests_factory.post(url, format='json', data=data)
        elif method.upper() == 'PUT':
            request = requests_factory.put(url, format='json', data=data)
        elif method.upper() == 'PATCH':
            request = requests_factory.patch(url, format='json', data=data)
        else:
            request = requests_factory.get(url, format='json', data=data)

        view = viewset_class.as_view({method.lower(): action})
        force_authenticate(request, user=auth_user, token=auth_user.auth_token)
        if pk is not None:
            return view(request, pk=pk, kwargs=data)
        return view(request, kwargs=data)
