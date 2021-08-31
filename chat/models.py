from datetime import datetime
from django.db import models, transaction
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Conversation(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   blank=False, null=False)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    participants = models.ManyToManyField(User,
                                          related_name='participants')

    class Meta:
        ordering = ['date_created']


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE,
                                     blank=False, null=False,
                                     related_name="messages")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='owner')
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    subject = models.CharField(max_length=128, blank=False, null=False)
    content = models.CharField(max_length=1024)

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
            participants = instance.conversation.participants.all().exclude(
                id=instance.created_by.id)
            [Recipient.objects.create(message=instance, recipient_user=recipient)
             for recipient in participants]


class Recipient(models.Model):
    message = models.ForeignKey(Message,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False,
                                related_name='recipients')
    recipient_user = models.ForeignKey(User,
                                       on_delete=models.CASCADE,
                                       blank=False,
                                       null=False)
    date_read = models.DateField(null=True)

    def is_read(self) -> bool:
        """returns boolean  if the message is read -> True"""
        return bool(self.date_read)

    def set_read(self) -> bool:
        """sets an instance as read (updates Message, date_read)"""
        with transaction.atomic():
            self.date_read = datetime.utcnow()
            self.save()
        return self.is_read()
