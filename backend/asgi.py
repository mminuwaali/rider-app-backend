import os
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from rideapp.routing import websocket_urlpatterns
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
    # "websocket": (AuthMiddlewareStack(URLRouter(websocket_urlpatterns))),
})
