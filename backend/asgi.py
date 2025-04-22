import os
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from your_app_name.routing import websocket_urlpatterns
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
})
