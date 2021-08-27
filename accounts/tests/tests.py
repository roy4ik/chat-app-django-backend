from django.test import TransactionTestCase
from accounts.models import User
# Create your tests here.


class UserProfileCreationTestCase(TransactionTestCase):

    def setUp(self):
        self.sender = User(
            username='jacob', email='jacob@gmail.com', password='top_secret')

    def profile_creation_test(self):
        self.setUp()
        assert self.sender
