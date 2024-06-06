import re

from django.db.models import QuerySet
from django.conf import settings
from channels.layers import get_channel_layer
from dataclasses import asdict
from asgiref.sync import async_to_sync

from chat.models import Chat, Message, UserChat
from chat.choices import CacheKeyChoices
from .types import UserData, UserInitChatDataT
from .additional_service import RequestsService, CacheService
from .decorators import cache_decorator
from chat.choices import ActionEnum

class ChatService:
    def __init__(self):
        self.cache_service = CacheService()
        self.blog_client_service = BlogClientService()

    @cache_decorator(CacheKeyChoices.CHAT_QUERYSET, timeout=60*60)
    def get_chat_queryset(self, user_id: int) -> QuerySet[Chat]:
        queryset = Chat.objects.filter(users__user=user_id)
        return queryset

    # def get_chat_queryset(self, user_id: int) -> QuerySet[Chat]:
    #     if queryset := self.cache_service.cache_get(CacheKeyChoices.CHAT_QUERYSET, version=user_id):
    #         return queryset
    #     queryset = Chat.objects.filter(users__user=user_id)
    #     self.cache_service.cache_set(value=queryset, timeout=60*60)
    #     return queryset

    def get_chat_messages_queryset(self, chat_id: str) -> QuerySet[Message]:
        return Message.objects.filter(chat_id=chat_id)

    def chat_init_request(self, jwt: str, user_id: str) -> dict:
        response = self.blog_client_service.init_chat(jwt=jwt, user_id=user_id)
        return response

    def typing_user_data(self, data: dict) -> UserInitChatDataT:
        user1 = UserData(**data[0])
        user2 = UserData(**data[1])
        return UserInitChatDataT(user1=user1, user2=user2)

    def create_models(self, data: UserInitChatDataT):
        chat_name = {
            data.user1.id: data.user2.full_name,
            data.user2.id: data.user1.full_name,
        }
        chat = Chat.objects.filter(users__user=data.user1.id).filter(users__user=data.user2.id).first()
        if chat:
            return chat

        chat = Chat.objects.create(name=chat_name)

        # вроде не должен вызывать ошибки если кэша с таким ключом нет
        self.cache_service.cache_delete(CacheKeyChoices.CHAT_QUERYSET, version=int(data.user1.id))
        self.cache_service.cache_delete(CacheKeyChoices.CHAT_QUERYSET, version=int(data.user2.id))

        user_chat_list = [
            UserChat(user=data.user1.id, chat=chat),
            UserChat(user=data.user2.id, chat=chat),
        ]
        UserChat.objects.bulk_create(user_chat_list)
        return chat

    def chat_handler(self, jwt: str, user_id: str):
        response = self.chat_init_request(jwt, user_id)
        user_data = self.typing_user_data(response)
        chat = self.create_models(user_data)
        self.notify_user(chat, user_data)
        return user_data

    @async_to_sync
    async def notify_user(self, chat: Chat, user_data: UserInitChatDataT):
        channel_layer = get_channel_layer()
        data = {
            'action': ActionEnum.CHAT_CREATED.value,
            'chat_id': chat.id,
            'init_user': asdict(user_data.user1)
        }
        await channel_layer.group_send(f'event_user_{user_data.user2.id}', {"type": "notify.user.new.chat", "data": data})
        return channel_layer

    def add_chat_avatar(self, queryset: QuerySet[Chat], user_id: int) -> QuerySet[Chat]:
        ids = {key for chat in queryset for key in chat.name.keys() if str(key) != str(user_id)}
        response = self.blog_client_service.get_users_data(ids)
        for chat in queryset:
            for user in response:
                if str(user['id']) in chat.name.keys():
                    chat.image = user['image']
        return queryset


class AsyncChatService:
    def __init__(self):
        self.service = BlogClientService()

    async def get_chats_id(self, user_id: int) -> QuerySet[Chat]:
        return Chat.objects.filter(users__user=user_id).values_list('id', flat=True)

    async def create_message(self, author: int, content: str, chat_id: str) -> Message:
        return await Message.objects.acreate(author=author, content=content, chat_id=chat_id)

    async def get_jwt(self, headers) -> str:
        """ Альтернативный метод получения jwt из headers."""
        headers = dict(headers)
        cookie = headers[b'cookie'].decode('utf-8')
        jwt = re.findall(r'(?<=jwt-auth=).+(?=; refresh=)', cookie)[0]
        return jwt

    async def get_user_by_jwt(self, jwt: str) -> UserData:
        data = self.service.get_cached_user_data_by_jwt(jwt)
        return UserData(**data)


class BlogClientService:
    def __init__(self, cache_service: CacheService = None):
        self.permission = settings.BLOG_HEADERS_PERMISSION
        self.base_url = settings.BLOG_URL
        self.requests_service = RequestsService()
        self.cache_service = cache_service

    def init_chat(self, jwt: str, user_id: str) -> dict:
        path = '/api/v1/chat/init-chat/'
        data = {'user_id': user_id, 'jwt_auth': jwt}
        url = self.requests_service.get_url(settings.BLOG_URL, path)
        response = self.requests_service.request(method='post', url=url, data=data)
        return response

    def get_users_data(self, ids: set) -> dict:
        params = {'user_ids': ','.join(ids)}
        path = '/api/v1/chat/users/'
        url = self.requests_service.get_url(base_url=settings.BLOG_URL, url=path)
        return self.requests_service.request(method='get', url=url, params=params)

    def get_user_data_by_jwt(self, jwt: str) -> dict:
        # if self.cache_service and (data := self.cache_service.cache_get(CacheKeyChoices.JWT, version=jwt)):
        #     print('get cache')
        #     return data
        path = '/api/v1/chat/user-data-by-jwt/'
        data = {'jwt_auth': jwt}
        url = self.requests_service.get_url(self.base_url, path)
        response_data = self.requests_service.request(method='post', url=url, data=data, headers=self.headers)
        # if self.cache_service:
        #     self.cache_service.cache_set(value=response_data)
        return response_data

    def get_user_data_by_id(self, id: int) -> dict:
        path = '/api/v1/chat/user-data-by-id/'
        data = {'id': id}
        url = self.requests_service.get_url(self.base_url, path)
        return self.requests_service.request(method='post', url=url, data=data, headers=self.headers)

    def get_cached_user_data_by_jwt(self, jwt: str) -> dict:
        if self.cache_service is None:
            self.cache_service = CacheService()
        if data := self.cache_service.cache_get(CacheKeyChoices.JWT, version=jwt):
            print('get cache')
            return data
        data = self.get_user_data_by_jwt(jwt)
        self.cache_service.cache_set(value=data)
        return data

    def get_cached_user_data_by_id(self, id: int) -> dict:
        if self.cache_service is None:
            self.cache_service = CacheService()
        if data := self.cache_service.cache_get(CacheKeyChoices.USER_ID, version=id):
            print('get cache')
            return data
        data = self.get_user_data_by_id(id)
        self.cache_service.cache_set(value=data, timeout=60*60)
        return data

    @property
    def headers(self):
        return {'Authorization': f'Token {self.permission}'}

    # methods = {
    #     'users_data': get_users_data,
    #     'user_data_by_jwt': get_user_data_by_jwt,
    #     'user_data_by_id': get_user_data_by_id,
    #     'cached_user_data_by_jwt': get_cached_user_data_by_jwt,
    #     'cached_user_data_by_id': get_cached_user_data_by_id
    # }
    #
    # def blog_client_handler(self, command: str, *data_or_params: str | int):
    #     return self.methods[command](self, *data_or_params)
