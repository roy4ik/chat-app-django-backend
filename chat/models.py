from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Conversation(models.Model):
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)


class Message(models.Model):
    conversation = models.OneToOneField(Conversation, on_delete=models.CASCADE, blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    is_active = models.BooleanField(default=True)
    subject = models.CharField(max_length=128, blank=False, null=False)
    content = models.CharField(max_length=1024)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')

    def __str__(self):
        return f'{self.id}: {self.created_by} -> {self.recipient}'
