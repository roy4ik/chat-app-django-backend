from datetime import datetime
from django.utils import timezone
from django.db import models, transaction
from django.contrib.auth.models import User


class Conversation(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_created']


class Message(models.Model):
    def __init__(self, *args, **kwargs):
        if kwargs.get("recipients") is not None:
            self.recipients_users = kwargs.pop("recipients")
        super().__init__(*args, **kwargs)

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE,
                                     blank=False, null=False,
                                     related_name="messages")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='owner')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=128, blank=False, null=False)
    content = models.CharField(max_length=1024)
    recipients = models.ManyToManyField(User, through='Recipient', through_fields=('message', 'recipient_user'))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.recipient_set.all():
            # skip if recipients exist (they cannot be added retroactively
            return
        if not self.recipients_users:
            raise ValueError('No recipient_users provided - required to save messages')
        self.recipients.set(self.recipients_users)

    def __str__(self):
        return f'{self.id}: {self.created_by}'

    class Meta:
        ordering = ['date_created']


class Recipient(models.Model):
    message = models.ForeignKey(Message,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False)
    recipient_user = models.ForeignKey(User,
                                       on_delete=models.CASCADE,
                                       blank=False,
                                       null=False)
    date_read = models.DateTimeField(null=True)

    def is_read(self) -> bool:
        """returns boolean  if the message is read -> True"""
        return bool(self.date_read)

    def set_read(self):
        """sets an instance as read (updates Message, date_read)"""
        if not self.is_read():
            with transaction.atomic():
                self.date_read = timezone.make_aware(datetime.utcnow(), timezone=timezone.utc)
                self.save()
        return self
