from django.test import TransactionTestCase
from accounts.models import User
from django.test import TestCase
# Create your tests here.


class UserProfileCreationTestCase(TestCase):

    def setUp(self):
        self.sender = User(
            username='jacob', email='jacob@gmail.com', password='top_secret')

    def test_profile_creation(self):
        self.setUp()
        assert self.sender
