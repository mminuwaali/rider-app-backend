from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/driver-location/", consumers.RiderLocationConsumer.as_asgi()),
    path("ws/rider-status/<request_id>/", consumers.RideStatusConsumer.as_asgi()),
]
