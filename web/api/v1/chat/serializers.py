from rest_framework import serializers

from chat.models import Chat, Message


class ChatSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    image = serializers.CharField()

    class Meta:
        model = Chat
        fields = ('id', 'name', 'created_at', 'user_id', 'image')

    def get_user_id(self, chat: Chat) -> int:
        return self.context['request'].user.id

    def get_name(self, chat: Chat) -> str:
        user = self.context['request'].user
        return chat.name[str(user.id)]

    # def get_image(self, chat: Chat) -> str:
    #     user_id = self.context['request'].user.id
    #     users = list(chat.users.values_list('user', flat=True))
    #     id = next(filter(lambda user: user != user_id, users))
    #     response_data = BlogClientService().get_cached_user_data_by_id(id)
    #     image = response_data['image']
    #     return image


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id',
            'author',
            'content',
            'created_at',
        )


class ChatInitSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
