from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_comma_separated_integer_list

class InvestorUser(AbstractUser):
    id          = models.AutoField(primary_key=True)
    watchlist   = models.CharField(validators=[validate_comma_separated_integer_list], max_length=200, default='[]', null=True, blank=True)
