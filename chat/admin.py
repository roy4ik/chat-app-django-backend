from django.contrib import admin

# Register your models here.
from accounts.models import Profile
from chat.models import Conversation, Message

admin.site.register(Profile)
admin.site.register(Conversation)
admin.site.register(Message)
