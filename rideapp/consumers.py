import json
from . import models
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from channels.generic.websocket import AsyncWebsocketConsumer


class RiderLocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "riders_location"

        if self.scope["user"] == AnonymousUser:
            await self.close()
            return

        # Add the user to the group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()


    async def disconnect(self, close_code):
        # Remove the user from the group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

        # Mark the rider as offline if it was set during the session
        if hasattr(self, "rider"):
            await database_sync_to_async(self.mark_rider_offline)(self.rider)


    async def receive(self, text_data):
        data = json.loads(text_data)
        item = data['data']

        print(data)

        rider = item["user"]
        latitude = item["latitude"]
        longitude = item["longitude"]

        self.rider = rider

        if data["action"] == "update_location":
            ...

            # Update rider's location
            await database_sync_to_async(self.update_rider_location)(
                rider, latitude, longitude
            )

        elif data["action"] == "send_location":
            # Update rider's location
            await database_sync_to_async(self.update_rider_location)(
                rider, latitude, longitude
            )

            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "broadcast_location",
                    "data": data["data"],
                },
            )

    async def broadcast_location(self, event):
        await self.send(text_data=json.dumps(event["data"]))

    def mark_rider_offline(self, rider):
        models.RiderLocation.objects.filter(rider_id=rider['id']).update(is_online=False)
        print(f"Marked rider {rider.id if rider else ''} as offline.")

    def update_rider_location(self, rider, latitude, longitude):
        print(rider)
        print("updating rider's location", rider,latitude, longitude)
        if latitude is None or longitude is None:
            print("no coordinates", latitude, longitude)
            return

        models.RiderLocation.objects.update_or_create(
            rider_id=rider['id'],
            defaults={"is_online":True, "latitude": latitude, "longitude": longitude}
        )


class RideStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract the request ID from the WebSocket URL
        self.request_id = self.scope["url_route"]["kwargs"]["request_id"]
        self.group_name = f"ride_status_{self.request_id}"

        print("Connected", self.request_id)

        # Add the WebSocket connection to the group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the WebSocket connection from the group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Handle incoming messages (if needed)
        data = json.loads(text_data)
        print(f"Received data: {data}")

        # Optionally broadcast the received data to the group
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "broadcast_status",
                "data": data,
            },
        )

    async def broadcast_status(self, event):
        # Broadcast the status update to the WebSocket group
        await self.send(text_data=json.dumps(event["data"]))
