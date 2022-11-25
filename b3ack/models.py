from django.db import models
from django.contrib.auth.models import AbstractUser

class InvestorUser(AbstractUser):
    id          = models.AutoField(primary_key=True)
    watchlist   = models.ManyToManyField('CompanyTracker', blank=True, related_name="watched_by")

class CompanyTracker(models.Model):
    id          = models.IntegerField(primary_key=True)
    api_id      = models.IntegerField() # Related ID in the API
    code        = models.CharField(max_length=64)
    name        = models.CharField(max_length=64)

    user        = models.ForeignKey(InvestorUser, on_delete=models.CASCADE, related_name="tracks")
    interval    = models.IntegerField(default=300) # Tracking interval in minutes

    # The following are all stores as lists, keeping track of the company's
    # data over time.
    abr         = models.JSONField(null=True, blank=True) # Opening value
    max         = models.JSONField(null=True, blank=True) # Maximum value
    min         = models.JSONField(null=True, blank=True) # Minimum value
    fch         = models.JSONField(null=True, blank=True) # Closing value
    capture_dt  = models.JSONField(null=True, blank=True) # Date and time data was registered

    # Maximum value at which user will be alerted to sell stocks
    sell_value  = models.FloatField(null=True, blank=True)
    # Minimum value at which user will be alerted to buy stocks 
    buy_value   = models.FloatField(null=True, blank=True)