import jwt
from django.conf import settings
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken

@database_sync_to_async
def get_user_from_token(token):
    try:
        # Validate the token
        user_model = get_user_model()
        validated_token = AccessToken(token)
        user = user_model.objects.get(id=validated_token['user_id'])
        return user
    except Exception as e:
        print(f"JWT Authentication Error: {e}")
        return AnonymousUser()


class JWTAuthMiddleware:
    """
    Middleware to authenticate a user using JWT token in WebSocket scope.
    """
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return JWTAuthMiddlewareInstance(scope, self.inner)

class JWTAuthMiddlewareInstance:
    def __init__(self, scope, inner):
        self.scope = scope
        self.inner = inner

    async def __call__(self, receive, send):
        query_string = self.scope.get("query_string", b"").decode("utf-8")
        query_params = dict(x.split("=") for x in query_string.split("&") if "=" in x)
        token = query_params.get("token", None)

        if token:
            self.scope["user"] = await get_user_from_token(token)
        else:
            self.scope["user"] = AnonymousUser()

        inner = self.inner(self.scope)
        return await inner(receive, send)
