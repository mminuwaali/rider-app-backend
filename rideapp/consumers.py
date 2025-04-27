import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DriverLocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.group_name = 'drivers_location'
        # await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        print("Connect set")
        await self.send(text_data="Connect set")

    async def disconnect(self, close_code):
        print("closing code",close_code)
        # await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
         # Parse the received JSON data
        data = json.loads(text_data)
        print(data)
        # Broadcast the data to the group
    #     await self.channel_layer.group_send(
    #         self.group_name,
    #         {
    #             "type": "location_update",  # Call the "location_update" method
    #             "message": data,           # Send the parsed data
    #         }
    #     )

    # async def location_update(self, event):
    #     await self.send(text_data=json.dumps(event))
        
