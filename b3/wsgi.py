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
# from b3ack.utils.tracking import Tracking
# import redis
# from b3.celery import app

# r = redis.Redis()
# r.flushdb()
# app.control.purge()

# Tracking(60).start_tracking()

application = get_wsgi_application()
