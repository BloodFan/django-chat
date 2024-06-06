from enum import Enum

from django.db.models import TextChoices


class ActionEnum(Enum):
    SEND_MESSAGE = 'send_message'
    WRITE_MESSAGE = 'write_message'
    CHAT_CREATED = 'chat_created'


class CacheKeyChoices(TextChoices):
    JWT = 'jwt'
    USER_ID = 'user_id'
    CHAT_QUERYSET = 'chat_queryset'


class CacheNameChoices(TextChoices):
    JWT = 'user.jwt'
    USER_ID = 'user.id'
    CHAT_QUERYSET = 'chat.queryset.user.id'
