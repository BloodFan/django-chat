from rest_framework.generics import GenericAPIView
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

from .serializers import ChatSerializer, MessageSerializer, ChatInitSerializer
from . authentications import JWTAuthentication
from .services import ChatService, BlogClientService
from .filters import ChatFilter
from chat.models import Message
from main.pagination import BasePageNumberPagination


class ChatAPIView(GenericAPIView):
    serializer_class = ChatSerializer
    pagination_class = BasePageNumberPagination
    filterset_class = ChatFilter
    permission_classes = []
    authentication_classes = (JWTAuthentication, )

    def get(self, request):
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)
        queryset_with_avatar = ChatService().add_chat_avatar(filtered_queryset, request.user.id)
        page = self.paginate_queryset(queryset_with_avatar)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def get_queryset(self):
        return ChatService().get_chat_queryset(self.request.user.id)


class ChatMessageAPIView(GenericAPIView):
    serializer_class = MessageSerializer
    permission_classes = []
    # authentication_classes = (SessionAuthentication,)
    authentication_classes = (JWTAuthentication,)

    def get(self, request, chat_id):
        queryset = Message.objects.annotate(chat_name=F('chat__name')).filter(chat_id=chat_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ChatInitView(GenericAPIView):
    """Инициализация чата."""
    serializer_class = ChatInitSerializer
    permission_classes = []

    @csrf_exempt
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {'user_id': serializer.data['user_id'], 'jwt': request.COOKIES['jwt-auth']}
        service = ChatService()
        service.chat_handler(**data)
        return Response(data)
