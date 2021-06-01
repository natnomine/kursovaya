from django.contrib import admin

from messenger.models import Chat, UserProfile, Message

admin.site.register(Chat)
admin.site.register(UserProfile)
admin.site.register(Message)
