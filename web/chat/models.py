from uuid import uuid4

from django.db import models


def hex_uuid() -> str:
    return uuid4().hex


# hex_uuid=lambda: uuid4().hex


class Chat(models.Model):
    id = models.CharField(max_length=32, primary_key=True, editable=False, db_index=True, default=hex_uuid)
    # name = models.CharField(max_length=50)
    name = models.JSONField(blank=True, null=True, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    # status

    def __str__(self):
        return f'{self.name}'


class Message(models.Model):
    author = models.PositiveIntegerField(db_index=True)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_ad
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')


class UserChat(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='users')
    user = models.PositiveIntegerField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=('chat', 'user'), name='unique user in chat')]

    def __str__(self):
        return f'{self.user}'
