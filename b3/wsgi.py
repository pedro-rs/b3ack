"""
WSGI config for b3 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'b3.settings')

# Startup
from b3ack.utils.tracking import Tracking
import redis
from b3.celery import app
from b3ack.models import CompanyTracker
from b3ack.utils.bcolors import bcolors

r = redis.Redis()
r.flushdb()
app.control.purge()

import django
django.setup()

# for ct in CompanyTracker.objects.all():
#     # Start tracking all companies
#     Tracking().start_tracking(ct.interval, ct.code, ct.id)
#     print(bcolors.WARNING + f"Tracking {ct.code} every {ct.interval / 60} minutes for {ct.user}!" + bcolors.ENDC)


application = get_wsgi_application()
