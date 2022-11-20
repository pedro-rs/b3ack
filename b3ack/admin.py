from django.contrib import admin
from .models import InvestorUser, Company

# Register your models here.
admin.site.register(InvestorUser)
admin.site.register(Company)