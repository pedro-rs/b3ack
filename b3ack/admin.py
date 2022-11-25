from django.contrib import admin
from .models import *

# Registering models.
admin.site.register(InvestorUser)
admin.site.register(CompanyTracker)