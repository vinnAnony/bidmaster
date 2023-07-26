import uuid
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.db import transaction


class Auctioneer(models.Model):
    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="auctioneer_account",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Auctioneer"
        verbose_name_plural = "Auctioneers"

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("auctioneer-detail", kwargs={"pk": self.pk})


class Bidder(models.Model):
    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="bidder_account",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Bidder"
        verbose_name_plural = "Bidders"

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("bidder-detail", kwargs={"pk": self.pk})


class Auction(models.Model):
    class AuctionStatus(models.IntegerChoices):
        ACTIVE = 1
        CLOSED = 0

    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    title = models.CharField(max_length=90, null=False, blank=False)
    description = models.TextField(null=True, blank=True, default="")
    auctioneer = models.ForeignKey(
        Auctioneer, related_name="auctions", on_delete=models.CASCADE
    )
    status = models.IntegerField(
        choices=AuctionStatus.choices, default=AuctionStatus.ACTIVE
    )
    winner = models.ForeignKey(
        Bidder,
        related_name="auctions",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Auction"
        verbose_name_plural = "Auctions"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("auction-detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        is_creating = self._state.adding
        if is_creating:
            self.create_auction_room()

        super().save(*args, **kwargs)

    @transaction.atomic
    def create_auction_room(self):
        auction_room = AuctionRoom(name=self.title, auction=self)
        auction_room.save()


class AuctionRoom(models.Model):
    class AuctionRoomStatus(models.IntegerChoices):
        ACTIVE = 1
        CLOSED = 0

    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(max_length=90, null=False, blank=False)
    status = models.IntegerField(
        choices=AuctionRoomStatus.choices, default=AuctionRoomStatus.ACTIVE
    )
    auction = models.OneToOneField(
        Auction, related_name="auction_acc", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Auction Room"
        verbose_name_plural = "Auction Rooms"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("auction-room-detail", kwargs={"pk": self.pk})


class AuctionRoomUser(models.Model):
    class AuctionRoomUserRole(models.TextChoices):
        ACTIONEER = "auctioneer"
        BIDDER = "bidder"

    auction_room = models.ForeignKey(AuctionRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    user_role = models.CharField(
        max_length=10, choices=AuctionRoomUserRole.choices, null=False, blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Auction Room User"
        verbose_name_plural = "Auction Room Users"

    def __str__(self):
        return f"{self.auction_room.name} > {self.user.username}"

    def get_absolute_url(self):
        return reverse("auction-room-user-detail", kwargs={"pk": self.pk})
