from channels.generic.websocket import AsyncJsonWebsocketConsumer

from api.v1.chat.services import AsyncChatService
from api.v1.chat.types import ChatMessageT, UserData
from chat.choices import ActionEnum


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.service = AsyncChatService()
        self.user: UserData = self.scope['user']

        chatList = await self.service.get_chats_id(self.user.id)

        room = f'event_user_{self.user.id}'
        await self.channel_layer.group_add(room, self.channel_name)

        async for chat in chatList:
            await self.channel_layer.group_add(chat, self.channel_name)
        await self.accept()

    # async def disconnect(self, close_code):
    # Leave room group
    # await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def send_message_handler(self, data: dict):
        user = self.user
        message = await self.service.create_message(author=user.id, content=data['content'], chat_id=data['chatId'])
        data['action'] = ActionEnum.SEND_MESSAGE.value
        data['author'] = str(user.id)
        data['created_at'] = str(message.created_at)
        await self.channel_layer.group_send(message.chat_id, {"type": "chat.message.event", "data": data})

    async def write_message_handler(self, data: dict):
        print(data, 'write_message_handler')
        data['action'] = ActionEnum.WRITE_MESSAGE.value
        await self.channel_layer.group_send(data['chatId'], {"type": "chat.message.event", "data": data})

    commands = {
        'sendMessage': send_message_handler,
        'startWriteMessage': write_message_handler,
    }

    async def receive_json(self, content: dict, **kwargs):
        # print(f'{content=}')
        command = content['command']
        await self.commands[command](self, content['data'])
        # await self.send_json(content)

        # Send message to room group
        # await self.channel_layer.group_send(
        #     self.room_group_name, {"type": "chat.message", "message": message}
        # )

    # Receive message from room group
    async def chat_message_event(self, event: ChatMessageT):
        print(event)
        # message = event["data"]["message"]
        await self.send_json(content=event['data'])

    async def notify_user_new_chat(self, event):
        print('notify', event)
        await self.send_json(content=event['data'])
