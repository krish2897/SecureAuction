from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

from .signals import auction_closed
# Create your models here.

class CustomUser(AbstractUser):

    is_auctioner = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    

class Auction(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="images/")
    base_price = models.IntegerField()
    auctioner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="auctioner_set")
    program_id = models.CharField(max_length=255)
    winner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="winner_set", blank=True, null=True)
    created_date = models.DateTimeField()
    ending_date = models.DateTimeField()
    is_closed = models.BooleanField(default=False)
    max_bids = models.IntegerField(default=4)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
            self.ending_date = self.created_date + timedelta(minutes=5)
        super(Auction, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def close_auction(self):
        self.is_closed = True
        self.save()
        auction_closed.send(sender=self.__class__, auction_id=self.id)

    def bid_count(self):
        return self.bidstoauction_set.count()

    def get_winner(self):
        if self.is_closed:
            return self.winner
        else:
            return None
    


class BidsToAuction(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bidder = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    store_id = models.CharField(max_length=255)
    bidding_date = models.DateTimeField(auto_now_add=True)
    bid_number = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('auction', 'bidder')


    def save(self, *args, **kwargs):
        super(BidsToAuction, self).save(*args, **kwargs)
        if self.auction.bidstoauction_set.count() >= self.auction.max_bids:
            self.auction.close_auction()
