from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_comma_separated_integer_list

class InvestorUser(AbstractUser):
    id          = models.AutoField(primary_key=True)
    watchlist   = models.ManyToManyField('CompanyTracker', blank=True, related_name="watched_by")

class CompanyTracker(models.Model):
    id          = models.IntegerField(primary_key=True)
    api_id      = models.IntegerField()
    code        = models.CharField(max_length=64)
    name        = models.CharField(max_length=64)

    user        = models.ForeignKey(InvestorUser, on_delete=models.CASCADE, related_name="tracks")
    interval    = models.IntegerField(default=300)

    abr         = models.JSONField(null=True, blank=True)
    max         = models.JSONField(null=True, blank=True)
    min         = models.JSONField(null=True, blank=True)
    fch         = models.JSONField(null=True, blank=True)
    capture_dt  = models.JSONField(null=True, blank=True)

    # create_date = models.DateTimeField(null=True)
    # categories  = models.ManyToManyField(Category, blank=true, related_name=???)