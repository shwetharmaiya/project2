from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    title = models.CharField(max_length=64)
    owner = models.CharField(max_length=64)
    desc = models.CharField(max_length=256)
    category = models.CharField(max_length=64)
    price = models.IntegerField()
    link = models.CharField(max_length=256,default=None,blank=True,null=True)
    time = models.CharField(max_length=64, default=timezone.now())

    class Meta:
        db_table="auctionlistings"

class Bids(models.Model):
    bidderinfo = models.CharField(max_length=64)
    bidamount = models.IntegerField()
    listingid = models.IntegerField()
    
class Comments(models.Model):
    user = models.CharField(max_length=64)
    time = models.CharField(max_length=64, default=timezone.now())
    comment = models.TextField()
    listingid = models.IntegerField()

class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()

class Closedbid(models.Model):
    owner = models.CharField(max_length=64)
    winner = models.CharField(max_length=64)
    listingid = models.IntegerField()
    winningprice = models.IntegerField()

class Alllisting(models.Model):
    listingid = models.IntegerField()
    title = models.CharField(max_length=64)
    description = models.TextField()
    link = models.CharField(max_length=256,default=None,blank=True,null=True)