from channels.sessions import CookieMiddleware

from api.v1.chat.services import AsyncChatService


class CookieAuthMiddleware:
    def __init__(self, app):
        print(f'{app=}')
        self.app = app

    async def __call__(self, scope, receive, send):
        self.service = AsyncChatService()
        jwt = scope['cookies']['jwt-auth']
        if not jwt:
            return
        user = await self.service.get_user_by_jwt(jwt)
        if user is None:
            return
        scope['user'] = user

        return await self.app(scope, receive, send)


def AuthMiddlewareStack(inner):
    return CookieMiddleware(CookieAuthMiddleware(inner))
