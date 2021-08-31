import datetime

from django.db import models, transaction
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver


# Create your models here.
class Conversation(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   blank=False, null=False)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    participants = models.ManyToManyField(User, related_name='participants')

    class Meta:
        ordering = ['date_created']


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    subject = models.CharField(max_length=128, blank=False, null=False)
    content = models.CharField(max_length=1024)
    recipients = models.ManyToManyField('Recipient', related_name='read_statuses')

    def __str__(self):
        return f'{self.id}: {self.created_by}'

    class Meta:
        ordering = ['date_created']


@receiver(post_save, sender=Message)
def set_initial_recipients(sender, created, instance, **kwargs):
    """sets the read statuses on the message for all participants of a conversation
        at the  time of message creation
     """
    if created:
        with transaction.atomic():
            participants = instance.conversation.participants.all().exclude(id=instance.created_by.id)
            instance.recipients.add(*[Recipient.objects.create(
                message=instance,
                recipient=recipient) for recipient in participants])


class Recipient(models.Model):
    message = models.ForeignKey(Message,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False)
    is_active = models.BooleanField(default=True)
    recipient = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  blank=False,
                                  null=False,
                                  related_name='recipient')
    date_read = models.DateField(null=True)

    def is_read(self):
        return bool(self.date_read)

    def set_read(self):
        with transaction.atomic():
            self.date_read = datetime.datetime.utcnow()
            self.save()
        return self.is_read()
