from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import AuctionRoom, AuctionRoomUser


@login_required
def index(request):
    if request.method == "POST":
        req_room_id = request.POST.get("room_id")
        req_user_id = request.user.id

        if not req_room_id:
            messages.error(request, "Please choose a valid room.")
            return redirect(reverse("bidding:index"))

        if room_exists(req_room_id):
            verified_room_user = verify_room_user(req_room_id, req_user_id)
            if verified_room_user["verified"]:
                return redirect(reverse("bidding:room",kwargs={"room_name": verified_room_user["room_name"]}))
            else:
                messages.error(request, "Not authorized to access room.")
                return redirect(reverse("bidding:index"))
        else:
            messages.error(request, "Room does not exist.")
            return redirect(reverse("bidding:index"))

    return render(request, "index.html")


@login_required
def room(request, room_name):
    return render(request, "room.html", {"room_name": room_name})


# check if room exists
def room_exists(room_id):
    try:
        return AuctionRoom.objects.filter(pk=room_id).exists()
    except:
        return False


# verify is user can access room
def verify_room_user(room_id, user_id):
    try:
        is_verified_room_user = AuctionRoomUser.objects.filter(auction_room=room_id, user=user_id)
        room_name = is_verified_room_user.first().auction_room.name
        
        return {
            "verified": is_verified_room_user.exists(),
            "room_name": room_name.lower().replace(" ", "_"),#convert room name into underscored name e.g. `My Room` to `my-room`
        }
    except:
        return False
