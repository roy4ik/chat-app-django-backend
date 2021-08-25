import datetime

from django.db import models, transaction
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver


# Create your models here.
class Conversation(models.Model):
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   blank=False, null=False)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    participants = models.ManyToManyField(User, related_name='participants')


class Message(models.Model):
    conversation = models.OneToOneField(Conversation, on_delete=models.CASCADE, blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    subject = models.CharField(max_length=128, blank=False, null=False)
    content = models.CharField(max_length=1024)
    read_statuses = models.ManyToManyField('ReadStatus')

    def __str__(self):
        return f'{self.id}: {self.created_by}'

    class Meta:
        ordering = ['date_created']


@receiver(post_save, sender=Message)
def set_read_statuses(sender, created, instance, **kwargs):
    """sets the read statuses on the message for all participants of a conversation
        at the  time of message creation
     """
    if created:
        with transaction.atomic():
            participants = instance.conversation.participants.all()
            instance.read_statuses.add(*[ReadStatus.objects.create(
                recipient=recipient) for recipient in participants])


class ReadStatus(models.Model):
    is_active = models.BooleanField(default=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name='recipient')
    date_read = models.DateField(null=True)

    def is_read(self):
        return bool(self.date_read)

    def set_read(self):
        self.date_read = datetime.datetime.utcnow()
        return self.is_read()
