from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Auctioneer)
admin.site.register(Bidder)
admin.site.register(Auction)
admin.site.register(AuctionRoom)
admin.site.register(AuctionRoomUser)
