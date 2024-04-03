from django.contrib import admin

from .models import Chat, UserChat, Message


class UserChatInline(admin.TabularInline):
    model = UserChat
    extra = 0

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    inlines = (UserChatInline,)


@admin.register(UserChat)
class UserChatAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass
