import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DriverLocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'drivers_location'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        latitude = data['latitude']
        longitude = data['longitude']
        driver_id = data['driver_id']

        # Save to the database (optional)
        # Notify all clients about the update
        await self.channel_layer.group_send(
            self.group_name,
            {
                'latitude': latitude,
                'driver_id': driver_id,
                'longitude': longitude,
                'type': 'location_update',
            }
        )

    async def location_update(self, event):
        await self.send(text_data=json.dumps({
            'latitude': event['latitude'],
            'driver_id': event['driver_id'],
            'longitude': event['longitude'],
        }))
