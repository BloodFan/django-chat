import asyncio

from rest_framework.authentication import BaseAuthentication

from .services import AsyncChatService


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        service = AsyncChatService()
        jwt = request.COOKIES['jwt-auth']
        if not jwt:
            return
        event_loop = asyncio.new_event_loop()
        user = event_loop.run_until_complete(service.get_user_by_jwt(jwt))
        if user is None:
            return
        return (user, None)
