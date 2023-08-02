from decimal import Decimal
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from bidding.models import AuctionLog,AuctionRoom

class BiddingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "bid_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        room_id = text_data_json["room_id"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "bid_message", "message": message,"username": username}
        )
        
        await self.insert_auction_log(room_id,Decimal(message))

    # Receive message from room group
    async def bid_message(self, event):
        message = event["message"]
        username = event["username"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message,"username":username}))

    @database_sync_to_async
    def insert_auction_log(self,room_id,amount:Decimal):
        auction_room = AuctionRoom.objects.get(pk=room_id)
        auction_log = AuctionLog.objects.create(
            auction_room_id = str(auction_room.id),
            user_id = str(self.user.id),
            amount = amount)
        
        auction_log.save()