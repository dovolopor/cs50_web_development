from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from auctions.templatetags.int_to_money import toMoney


class User(AbstractUser):
    watchlist = models.ManyToManyField('Auction', related_name="watched_by")

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    imagePath = models.CharField(max_length=1024, null=True, blank=True)
    creator = models.ForeignKey(User,on_delete=models.CASCADE, related_name="auctions")
    category = models.CharField(max_length=64, null=True, blank=True)
    openingPrice = models.IntegerField(default=0)
    startTime = models.DateTimeField(default = datetime.now, auto_now=False, blank= False)
    endTime = models.DateTimeField(default= datetime.now, auto_now=False, blank=False)


    def __str__(self):
        return f"{self.title}"

    def priceStr(self):
        return "3"

class Bid(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="bids")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    price = models.IntegerField(default=0)

    def __str__(self):
        return f"${toMoney(self.price)} by {self.user} for {self.auction.title}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=256)
    def __str__(self):
        return f"{self.text[:5]} by {self.user}"