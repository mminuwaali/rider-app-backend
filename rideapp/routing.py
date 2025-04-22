from . import consumers
from django.urls import path

websocket_urlpatterns = [
    path('ws/driver-location/', consumers.DriverLocationConsumer.as_asgi()),
]
